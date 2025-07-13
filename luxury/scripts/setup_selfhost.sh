
#!/bin/bash
# Usage: ./setup_selfhost.sh panel.redteam.lab

DOMAIN=$1

echo "[*] Installing Nginx and Certbot..."
sudo apt update && sudo apt install nginx certbot python3-certbot-nginx -y

echo "[*] Copying NGINX config..."
sudo cp nginx_conf_template.conf /etc/nginx/sites-available/$DOMAIN
sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/

echo "[*] Replacing domain in config..."
sudo sed -i "s/panel.redteam.lab/$DOMAIN/g" /etc/nginx/sites-available/$DOMAIN

echo "[*] Restarting NGINX..."
sudo systemctl restart nginx

echo "[*] Requesting Let's Encrypt certificate..."
sudo certbot --nginx -d $DOMAIN

echo "[*] Done. Your C2 should now be live at: https://$DOMAIN"
