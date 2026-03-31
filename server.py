import socket
import json,time
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

AES_KEY = b"0123456789ABCDEF0123456789ABCDEF"   # EXACT same as client
assert len(AES_KEY) == 32 # AES-256 requires a 32-byte key
aesgcm = AESGCM(AES_KEY)

def run_server():

    print("AES SEVER VERSION ACTIVE")

    HOST ="0.0.0.0" #listen to all interfaces 
    PORT=9999

    server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # AF_INET-IPV4 ADDRESS, SOCK_DGRAM=UDP CONNECTION
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows rebinding after restart
    server_socket.bind((HOST,PORT)) # BINDING UDP TO PARTICULAR HOST AND PORT

    print(f"UDP Server listening on{HOST}:{PORT}\n")

    BATCH_SIZE=5 #maximum logs which buffer can contain
    MAX_BUFFER_SIZE=20 #if logs arrive faster size increases so if >20 then we drop some logs

    log_buffer=[] #store logs temporarily for sorting
    all_logs=[]   # store all logs for analysis
    total_logs=0 #total logs processed
    start_time=None #time-elaspsed
    FAIL_AFTER=20

    while True:
        
        data, addr = server_socket.recvfrom(4096)

        try:
          nonce = data[:12]
          ciphertext = data[12:]
          plaintext = aesgcm.decrypt(nonce, ciphertext, None)
          log = json.loads(plaintext.decode())
        except Exception:
          continue   # DROP BAD PACKETS, NO FALLBACK

        if start_time is None:
            start_time=time.time()

        log_buffer.append(log)
        all_logs.append(log)

        # SAVE TO FILE
        with open("logs.json", "a") as f:
            f.write(json.dumps(log) + "\n")

        buffer_size = len(log_buffer)

        if buffer_size > 0.7 * MAX_BUFFER_SIZE:
            print("Warning: Buffer almost full")

        if buffer_size > 0.9 * MAX_BUFFER_SIZE:
            print("Critical: System overloaded")

        # PROCESS ONLY A PART OF BUFFER (IMPORTANT CHANGE)
        if len(log_buffer) >= BATCH_SIZE:
            batch = log_buffer[:BATCH_SIZE]
            batch.sort(key=lambda x:x['timestamp'])

            for x in batch:
                time_str = datetime.fromtimestamp(x['timestamp']).strftime("%H:%M:%S.%f")[:-3]
                print(f"[{x['machine_ip']}] {time_str} {x['level']} - {x['message']}")

            total_logs += len(batch)

            current_time=time.time()
            elapse_time=current_time-start_time
            throughput=total_logs/elapse_time

            print(f"The throughput is {throughput:.2f} logs/sec\n")

            log_buffer = log_buffer[5:]

        # TIME-BASED FAILURE (but message says buffer overflow)
        if start_time is not None and time.time() - start_time > FAIL_AFTER:
            print("Failure: Buffer overflow due to high incoming log rate")

            print("\nFlushing remaining logs before shutdown:\n")

            log_buffer.sort(key=lambda x:x['timestamp'])
            for x in log_buffer:
                time_str = datetime.fromtimestamp(x['timestamp']).strftime("%H:%M:%S.%f")[:-3]
                print(f"[{x['machine_ip']}] {time_str} {x['level']} - {x['message']}")
                time.sleep(0.2)

            server_socket.close()
            return   # exit function → restart

        time.sleep(0.5)


# AUTOMATIC RECOVERY LOOP WITH 5 SECOND GAP
while True:
    run_server()
    print("Recovery: Restarting server in 5 seconds...")
    time.sleep(5)
