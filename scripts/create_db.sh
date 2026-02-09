#/bin/bash

# DB vars
DB_NAME="practica"
DB_USER="joelsansi"
DB_PASS="1234"

cat mysql <<EOF > db.sql
DROP DATABASE IF EXISTS ${DB_NAME};

CREATE DATABASE ${DB_NAME} CHARACTER SET utf8mb4;
USE ${DB_NAME};

DROP USER IF EXISTS '${DB_USER}'@'localhost';

CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';

GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

sudo mysql < db.sql

