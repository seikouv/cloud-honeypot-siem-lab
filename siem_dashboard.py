import os
import re
from collections import Counter

LOG_FILE = "honeypot_activity.log"

def analyze_logs():
    if not os.path.exists(LOG_FILE):
        print("[-] No log file found. Run the honeypot first!")
        return

    print("=" * 50)
    print("      MINI-SIEM SECURITY DASHBOARD       ")
    print("=" * 50)

    total_alerts = 0
    attack_payloads = []
    user_agents = []

    # Read and parse the log file
    with open(LOG_FILE, "r") as f:
        for line in f:
            if "[ATTACK_DETECTED]" in line:
                total_alerts += 1
                
                # Extract specific details using regex/string parsing
                if "Payload Sent:" in line:
                    payload = line.split("Payload Sent:")[1].strip()
                    # Grab just the first line of the HTTP payload for brevity
                    first_line = payload.split("\n")[0]
                    attack_payloads.append(first_line)
                
                if "User-Agent:" in line:
                    try:
                        agent = line.split("User-Agent:")[1].split("\n")[0].strip()
                        user_agents.append(agent[:50] + "...") # Truncate for clean view
                    except IndexError:
                        pass

    print(f"Total Security Incidents Logged: {total_alerts}")
    print("-" * 50)

    # Metric 1: Top Attack Vectors / Payloads
    print("\nTOP ATTACK VECTORS (URIs/Payloads):")
    payload_counts = Counter(attack_payloads)
    for payload, count in payload_counts.most_common(5):
        print(f"  [{count}x] -> {payload}")

    # Metric 2: Top Attacker Tools Used
    print("\nMOST COMMON ATTACKER TOOLS / USER-AGENTS:")
    agent_counts = Counter(user_agents)
    for agent, count in agent_counts.most_common(3):
        print(f"  [{count}x] -> {agent}")
        
    print("=" * 50)

if __name__ == "__main__":
    analyze_logs()