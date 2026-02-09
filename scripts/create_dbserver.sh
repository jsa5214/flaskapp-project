#/bin/bash

# Install mysql_server
sudo apt update && sudo apt install mysql-server -y

sudo systemctl start mysql && sudo systemctl enable mysql

sudo mkdir -p /var/www/flaskapp/sql

# Emulate mysql_secure_installation
sudo mysql <<EOF
DELETE FROM mysql.user WHERE User='';

UPDATE mysql.user SET Host='localhost' WHERE User='root';

DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "DB Created succesfully"

else
    echo "Error"
fi

