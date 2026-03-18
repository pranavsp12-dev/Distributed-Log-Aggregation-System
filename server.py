import socket
import json,time
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
AES_KEY = b"0123456789ABCDEF0123456789ABCDEF"   # EXACT same as client
assert len(AES_KEY) == 32 # AES-256 requires a 32-byte key
aesgcm = AESGCM(AES_KEY)
print("AES SEVER VERSION ACTIVE")
HOST ="0.0.0.0" #listen to all interfaces 
PORT=9999
server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # AF_INET-IPV4 ADDRESS, SOCK_DGRAM=UDP CONNECTION
server_socket.bind((HOST,PORT)) # BINDING UDP TO PARTICULAR HOST AND PORT
print(f"UDP Server listening on{HOST}:{PORT}\n")
BATCH_SIZE=20 #maximum logs which buffer can contain
MAX_BUFFER_SIZE=5 #if logs arrive faster size increases so if >20 then we drop some logs
log_buffer=[] #store logs temporarily for sorting
total_logs=0 #total logs processed
start_time=None #time-elaspsed
while True:
    
    data, addr = server_socket.recvfrom(4096)

    try:
      nonce = data[:12]
      ciphertext = data[12:]
      plaintext = aesgcm.decrypt(nonce, ciphertext, None)
      log = json.loads(plaintext.decode())
    except Exception:
      continue   # DROP BAD PACKETS, NO FALLBACK
    if len(log_buffer)<MAX_BUFFER_SIZE:
         if start_time is None:
             start_time=time.time()
         log_buffer.append(log)
         if len(log_buffer)>=BATCH_SIZE:
            log_buffer.sort(key=lambda x:x['timestamp'])
            for x in log_buffer:
                  time_str = datetime.fromtimestamp(x['timestamp']).strftime("%H:%M:%S.%f")[:-3]
                  print(f"[{x['machine_ip']}] {time_str} {x['level']} - {x['message']}")

            total_logs+=len(log_buffer)
            current_time=time.time()
            elapse_time=current_time-start_time
            throughput=total_logs/elapse_time
            print(f"The throughput is{throughput:.2f}logs/sec")

            log_buffer.clear()
    else:
        print("Maximum capacity reached. Dropping logs..!")


