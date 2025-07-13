import threading
import subprocess
import os
import time
from datetime import datetime

# Paths to scripts (adjust if needed)
MODULES = {
    "Keylogger": "keylogger_lab.py",
    "Screen Capture": "screencap_sim.py",
    "Microphone Recorder": "mic_grabber.py",
    "DNS Exfil Simulator": "dns_exfil_sim.py",
}

ENABLED = {
    "Keylogger": True,
    "Screen Capture": True,
    "Microphone Recorder": True,
    "DNS Exfil Simulator": False,  # Toggle on as needed
}

LOG_FILE = "launcher_status.log"

def log(msg):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[+] {msg}")

def run_script(name, path):
    try:
        log(f"Starting {name} -> {path}")
        subprocess.Popen(["python", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        log(f"Error starting {name}: {e}")

def main():
    log("=== Launching Simulation Modules ===")

    for name, script in MODULES.items():
        if ENABLED.get(name):
            t = threading.Thread(target=run_script, args=(name, script))
            t.start()
            time.sleep(1)  # slight delay to stagger startup

    log("All enabled modules launched.\n")

if __name__ == "__main__":
    main()
