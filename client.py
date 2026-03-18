import socket
import json,time
import random
import os
import sys 
from datetime import datetime
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
AES_KEY = b"0123456789ABCDEF0123456789ABCDEF"   # EXACT same on server
assert len(AES_KEY) == 32 # AES-256 requires a 32-byte key
aesgcm = AESGCM(AES_KEY)
SERVER_IP="127.0.0.1"
SERVER_PORT=9999

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# get real machine IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
machine_ip = s.getsockname()[0] #get local ip
s.close()
log_levels = ["DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"]
log_messages = {
    "DEBUG": [
        "Entering authentication module",
        "Fetching user details from cache",
        "Loop iteration started",
        "Parsing configuration file",
        "Connection object initialized"
    ],
    "INFO": [
        "User login successful",
        "Service started successfully",
        "Connection established with server",
        "Scheduled job executed",
        "Configuration loaded successfully"
    ],
    "NOTICE": [
        "System running in maintenance mode",
        "Background cleanup task scheduled",
        "New device registered",
        "Cache refreshed successfully",
        "Heartbeat signal received"
    ],
    "WARNING": [
        "High memory usage detected",
        "Disk space running low",
        "CPU utilization exceeded threshold",
        "Slow response from database",
        "Network latency above normal levels"
    ],
    "ERROR": [
        "Database connection failed",
        "File not found error",
        "Timeout occurred while processing request",
        "Invalid user credentials provided",
        "Failed to write data to disk"
    ],
    "CRITICAL": [
        "System crash detected",
        "Data corruption detected",
        "Service unavailable",
        "Critical dependency failure",
        "Kernel module failure detected"
    ],
    "ALERT": [
        "Security breach suspected",
        "Unauthorized access attempt detected",
        "Firewall rule violation",
        "Multiple failed login attempts",
        "Abnormal traffic spike detected"
    ],
    "EMERGENCY": [
        "System unusable",
        "Kernel panic triggered",
        "All services down",
        "Database completely unreachable",
        "Emergency shutdown initiated"
    ]
}
#machine_ids=["M1","M2","M3","M4","M5","M6","M7"]
while True:
    for _ in range(7):
        #machine_id=random.choice(machine_ids)
        current_time=datetime.now()
        level=random.choice(log_levels)
        message=random.choice(log_messages[level])
        log_message={
        "machine_ip":machine_ip,
        "timestamp": time.time(),
        "datetime" : current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "level":level,
        "message":message
    }
        plaintext = json.dumps(log_message).encode()
        nonce = os.urandom(12)

        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        packet = nonce + ciphertext

        client_socket.sendto(packet, (SERVER_IP, SERVER_PORT))
        time.sleep(0.02)
    time.sleep(1) #pauses client for 1 second before sending next log

