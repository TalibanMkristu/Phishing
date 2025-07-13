import pyautogui
import time
import os
from datetime import datetime

SAVE_DIR = "screens/"
INTERVAL = 30  # seconds

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

print("[*] Starting screen capture simulation...")

while True:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join(SAVE_DIR, f"{timestamp}.png")
    pyautogui.screenshot(path)
    print(f"[+] Screenshot saved to {path}")
    time.sleep(INTERVAL)
