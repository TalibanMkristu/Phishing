import os, shutil

def safe_delete(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

clean_paths = ['keystrokes.log', 'launcher_status.log', 'screens/', 'audio_logs/']

for p in clean_paths:
    safe_delete(p)
print("[+] Simulation artifacts cleaned.")