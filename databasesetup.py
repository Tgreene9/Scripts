#!/bin/bash

# Install PostgreSQL packages
sudo dnf install -y postgresql-server postgresql-contrib libpq-devel python3 python3-pip

# Initialize the PostgreSQL database
sudo postgresql-setup initdb

# Install psycopg2 using pip
sudo pip3 install psycopg2

# Start and enable PostgreSQL service
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Configure PostgreSQL to listen on all interfaces
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /var/lib/pgsql/data/postgresql.conf

# Set PostgreSQL password for the PostgreSQL user
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'SuperS3cur3P@ssw0rd!!'"

# Allow PostgreSQL port in firewall
sudo firewall-cmd --zone=public --add-port=5432/tcp --permanent
sudo firewall-cmd --reload

# Allow all IPs to connect to PostgreSQL
echo "host    all             all             0.0.0.0/0               md5" | sudo tee -a /var/lib/pgsql/data/pg_hba.conf

# Create a PostgreSQL database
sudo -u postgres createdb -E UTF8 -l en_US.UTF-8 -T template0 db

# Change PostgreSQL port
sudo sed -i "s/#port = 5432/port = 5432/g" /var/lib/pgsql/data/postgresql.conf

# Restart PostgreSQL service
sudo systemctl restart postgresql

echo "PostgreSQL setup completed successfully!"
