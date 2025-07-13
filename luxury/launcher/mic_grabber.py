import sounddevice as sd
from scipy.io.wavfile import write
import os
import time
from datetime import datetime

SAVE_DIR = "audio_logs/"
DURATION = 10  # seconds

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

print("[*] Recording mic audio every minute...")

while True:
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = os.path.join(SAVE_DIR, f"mic_{timestamp}.wav")

    print(f"[+] Recording {DURATION}s audio to {file_path}")
    audio = sd.rec(int(DURATION * 44100), samplerate=44100, channels=2)
    sd.wait()
    write(file_path, 44100, audio)

    time.sleep(60)
