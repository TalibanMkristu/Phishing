
# redphish-phishing-lab

🎯 **Red Team Phishing + Browser C2 Simulation Lab**  
A Django-based phishing framework featuring:

- ✅ Realistic login page clones (Gmail, Facebook, Microsoft)
- 🧠 JS-based C2 beacon with command execution
- 🔐 Automatic JavaScript obfuscation (via `javascript-obfuscator`)
- 🧪 Reverse shells via WebSocket or Netcat POST fallback
- 📡 Live credential capture viewer at `/admin/live-log/`
- 🔒 Full HTTPS setup via Nginx + Certbot + DuckDNS

## 🔧 Quick Setup

```bash
curl -sL redphish.sh | bash
```

> Set your domain inside `redphish.sh` or pass `--domain yourdomain.duckdns.org`

## 🧪 Features

| Feature                     | Description                                               |
|----------------------------|-----------------------------------------------------------|
| 🔐 JS Obfuscation          | `client.js` auto-obfuscated as `beacon.ob.js`             |
| 🎣 Phishing Pages          | Realistic clones with logos, fonts, CSS                   |
| 🖥️ Web UI C2 Panel         | Command interface for browser-controlled clients          |
| 🔁 Reverse Shells          | WebSocket + Netcat fallback over HTTPS                    |
| 📺 Live Log Viewer         | View captured credentials live via admin page             |
| 🧩 WASM & Payload Loader   | Easily extendable with encrypted loaders                  |

## 🌐 Pages

| Path                     | Purpose                    |
|--------------------------|----------------------------|
| `/gmail/`                | Fake Gmail login           |
| `/facebook/`             | Fake Facebook login        |
| `/microsoft/`            | Fake Microsoft login       |
| `/admin/live-log/`       | Live credential viewer     |

## 📦 Includes

- `redphish/` Django app
- `templates/` with clones
- `static/js/` payloads
- `ws_shell_server.py`
- `netcat_fallback.py`
- `redphish.sh` installer

## 📜 Legal Warning

This project is for **educational and authorized red team training use only**. Do **not** deploy against live systems without **explicit permission**.