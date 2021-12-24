cp /var/www/application/pi-sensor-v2/nginx/application.conf /etc/nginx/sites-available/application.conf
cp /var/www/application/pi-sensor-v2/nginx/application.service /etc/systemd/system/application.service
cp /var/www/application/pi-sensor-v2/fail2ban/jail.local /etc/fail2ban

sudo systemctl enable application.service
sudo systemctl restart nginx
sudo systemctl restart application.service
sudo systemctl daemon-reload