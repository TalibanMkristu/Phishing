#!/bin/bash
# Start Django server and expose via ngrok

echo "[*] Starting Django server on 127.0.0.1:8000..."
python manage.py runserver &

sleep 5
echo "[*] Launching ngrok tunnel..."
ngrok http 8000
