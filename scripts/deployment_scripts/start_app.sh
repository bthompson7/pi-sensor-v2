sudo systemctl enable application.service
sudo systemctl restart nginx
sudo systemctl restart application.service
sudo systemctl daemon-reload