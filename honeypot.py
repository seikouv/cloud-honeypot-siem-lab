import socket
import logging
from datetime import datetime

# 1. Set up a professional security log file
logging.basicConfig(
    filename='honeypot_activity.log',
    level=logging.INFO,
    format='%(asctime)s - [ATTACK_DETECTED] - %(message)s'
)

def start_honeypot():
    # Listen on port 8080 (a common target port for web app attacks)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    
    print("[*] Honeypot is live and listening on port 8080...")
    
    while True:
        client_socket, client_address = server.accept()
        attacker_ip = client_address[0]
        attacker_port = client_address[1]
        
        # Log the attack details
        log_message = f"Source IP: {attacker_ip} | Target Port: 8080 | Connection Attempt Established."
        print(f"{log_message}")
        logging.info(log_message)
        
        # Send a fake banner back to trick the hacker
        try:
            client_socket.send(b"HTTP/1.1 200 OK\nServer: Apache/2.4.41 (Ubuntu)\n\nWelcome to Admin Portal.\n")
            # Capture what the hacker types
            data = client_socket.recv(1024)
            if data:
                payload_message = f"Source IP: {attacker_ip} | Payload Sent: {data.decode('utf-8', errors='ignore').strip()}"
                print(f"Data Captured: {payload_message}")
                logging.info(payload_message)
        except Exception as e:
            pass
            
        client_socket.close()

if __name__ == "__main__":
    start_honeypot()