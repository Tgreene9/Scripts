#!/bin/bash

# Update and install required packages
sudo apt update
sudo apt install -y python3 python3-pip libpq-dev git

# Clone the repository
git clone https://gitlab.com/c2-games/red-team/web-apps/the-music-store /tmp/music_shop
cd /tmp/music_shop

# Create a directory for the web application
sudo mkdir -p /var/lib/music_shop
sudo chown -R root:root /var/lib/music_shop
sudo chmod 0755 /var/lib/music_shop

# Copy the source code to the web application directory
sudo cp -r requirements.txt main.py config.py app static templates /var/lib/music_shop/
sudo chown -R root:root /var/lib/music_shop
sudo chmod 0755 /var/lib/music_shop

# Create the .env file
sudo tee /var/lib/music_shop/.env > /dev/null <<EOT
SITE_NAME=The Music Shop

WEB_APP_PORT=80
WEB_APP_HOST=0.0.0.0

POSTGRES_HOST=<your-postgres-host-ip>
POSTGRES_PORT=5432
POSTGRES_DB=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=SuperS3cur3P@ssw0rd!!

WERKZEUG_DEBUG_PIN=off
EOT

# Install the Python packages
sudo pip3 install -r /var/lib/music_shop/requirements.txt

# Create the systemd service file
sudo tee /etc/systemd/system/music_shop.service > /dev/null <<EOT
[Unit]
Description=Flask Web Application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/lib/music_shop
ExecStart=/usr/bin/python3 main.py

[Install]
WantedBy=multi-user.target
EOT

# Reload the systemd daemon and start the service
sudo systemctl daemon-reload
sudo systemctl enable music_shop
sudo systemctl start music_shop

# Clean up
cd ~
rm -rf /tmp/music_shop

echo "Flask web application setup completed successfully!"
