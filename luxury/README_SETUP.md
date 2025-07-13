
# Browser C2 + Phishing Clone + Monitor (Django)

## Setup
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py runserver

## Apps:
- /phish/ : Realistic login page clone
- /c2/ : JS beacon listener and injector
- /monitor/ : Tracks JS exfil, fetch(), WebSocket, beacon

## Optional:
- Use ngrok for external access
