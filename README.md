Distributed Log Aggregation System
Project Overview

This project implements a Distributed Log Aggregation System using UDP communication and AES-GCM encryption.

Multiple simulated client machines generate encrypted logs and send them to a centralized server. The server decrypts, buffers, sorts the logs by timestamp, and calculates throughput.

Features

a. UDP-based communication

b. AES-GCM (256-bit) encryption

c. Unique 12-byte nonce per message

d. Log batching (20 logs per batch)

e. Timestamp-based sorting

f. Real-time throughput calculation

g. Buffer overflow protection

h. Simulated multiple machines

Technologies Used

Python

Socket Programming (UDP)

JSON

Cryptography Library (AES-GCM)

distributed-log-aggregation/
│
├── client.py
├── server.py
├── requirements.txt
└── README.md

Installation
1. Clone the Repository
    git clone https://github.com/your-username/distributed-log-aggregation.git
    cd distributed-log-aggregation

2.Install Dependencies
    pip install -r requirements.txt

How to Run
Step 1: Start the Server

Open a terminal and run: python server.py

Step 2: Start the Client

Open another terminal and run: python client.py

Example Output
UDP Server listening on 0.0.0.0:9999

[M2] 2026-02-25 10:14:01 (Tuesday) INFO - Service started successfully
[M4] 2026-02-25 10:14:01 (Tuesday) WARNING - High memory usage detected
[M1] 2026-02-25 10:14:01 (Tuesday) DEBUG - Parsing configuration file
[M6] 2026-02-25 10:14:02 (Tuesday) ERROR - Database connection failed
[M3] 2026-02-25 10:14:02 (Tuesday) NOTICE - Cache refreshed successfully
[M5] 2026-02-25 10:14:02 (Tuesday) ALERT - Unauthorized access attempt detected
[M7] 2026-02-25 10:14:03 (Tuesday) CRITICAL - Service unavailable
[M2] 2026-02-25 10:14:03 (Tuesday) EMERGENCY - System unusable

The throughput is 50.12 logs/sec

Security

Logs are encrypted using AES-GCM (256-bit key) which provides:

Confidentiality

Integrity

Authentication

Each log message uses a unique 12-byte nonce to ensure secure encryption.

Team Members
NAME- PRANAV SP
SRN-  PES1UG24CS337

NAME-RAMITH MUNNAN RAVINDRANATH
SRN-PES1UG24CS367

NAME-Ojas Binjola
SRN-PES1UG24CS307

COURSE NAME -Computer Networks
COURSE CODE- UE24CS252B 