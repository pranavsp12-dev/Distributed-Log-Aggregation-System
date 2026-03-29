Distributed Log Aggregation System

Project Overview

This project implements a Distributed Log Aggregation System using UDP communication and AES-GCM encryption.

Multiple client machines (simulated using different IP addresses) generate encrypted logs and send them to a centralized server. The server decrypts, buffers, sorts logs based on timestamps, and calculates throughput.

A Streamlit dashboard is also included to analyze logs in real time.

---

Features

- UDP-based communication
- AES-GCM (256-bit) encryption
- Unique 12-byte nonce per message
- Log batching and buffering
- Timestamp-based sorting
- Real-time throughput calculation
- Buffer overflow detection and failure simulation
- Automatic server recovery
- Multi-client simulation
- Logs tagged with real machine IP addresses
- Streamlit-based log analysis dashboard

---

Technologies Used

- Python
- Socket Programming (UDP)
- JSON
- Cryptography Library (AES-GCM)
- Streamlit
- Pandas
- Matplotlib

---

Project Structure

distributed-log-aggregation-system/

client.py        Simulates multiple log-generating machines  
server.py        Receives, decrypts, buffers, and processes logs  
app.py           Streamlit dashboard for log analysis  
logs.json        Generated log data (not tracked in Git)  
requirements.txt  
README.md  

---

Installation

1. Clone the repository

git clone https://github.com/pranavsp12-dev/Distributed-Log-Aggregation-System.git  
cd Distributed-log-aggregation-system  

2. Install dependencies

pip install -r requirements.txt  

---

How to Run

Step 1: Start the Server

python server.py  

Step 2: Start the Client

python client.py  

Step 3: Run the Dashboard

streamlit run app.py  

---

Example Output

UDP Server listening on 0.0.0.0:9999  

[192.168.29.40] 16:46:52.157 INFO - Service started successfully  
[192.168.29.41] 16:46:52.178 WARNING - High memory usage detected  
[192.168.29.42] 16:46:52.199 DEBUG - Parsing configuration file  
[192.168.29.43] 16:46:52.220 ERROR - Database connection failed  
[192.168.29.44] 16:46:52.241 NOTICE - Cache refreshed successfully  
[192.168.29.45] 16:46:52.262 ALERT - Unauthorized access attempt detected  
[192.168.29.46] 16:46:52.283 CRITICAL - Service unavailable  
[192.168.29.47] 16:46:52.304 EMERGENCY - System unusable  

The throughput is 50.12 logs/sec  

---

Security

Logs are encrypted using AES-GCM with a 256-bit key, which provides confidentiality, integrity, and authentication.

Each log message uses a unique 12-byte nonce to ensure secure encryption.

---

Team Members

Pranav SP  
SRN: PES1UG24CS337  

Ramith Munnan Ravindranath  
SRN: PES1UG24CS367  

Ojas Binjola  
SRN: PES1UG24CS307  

---

Course Details

Course Name: Computer Networks  
Course Code: UE24CS252B  
