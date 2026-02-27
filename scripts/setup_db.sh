#!/bin/bash

# Aquest script instal·la MySQL (si no hi és) i configura la base de dades.
# Ha de ser executat amb sudo si cal instal·lar paquets, o amb permisos per a mysql.

echo "Verificant si MySQL està instal·lat..."
if ! command -v mysql &> /dev/null; then
    echo "MySQL no està instal·lat. Instal·lant mysql-server..."
    sudo apt-get update
    sudo apt-get install -y mysql-server
    
    echo "Iniciant el servei de MySQL..."
    sudo systemctl start mysql
    sudo systemctl enable mysql
else
    echo "MySQL ja està instal·lat."
fi

echo "Configurant la base de dades i l'usuari..."
# Creem la BD, l'usuari i donem permisos directament amb root
sudo mysql -e "CREATE DATABASE IF NOT EXISTS \`flaskapp_db\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY 'flask_pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON \`flaskapp_db\`.* TO 'flask_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "Important l'esquema inicial i dades de prova (scripts/db.sql)..."
# Comprovem si l'arxiu existeix
if [ -f "scripts/db.sql" ]; then
    # Inserim el contingut
    sudo mysql flaskapp_db < scripts/db.sql
    echo "Dades de prova (dummy data) carregades correctament."
else
    echo "No s'ha trobat scripts/db.sql. La base de dades s'ha creat, però està buida."
fi

echo "================================================="
echo "Configuració de la Base de Dades completada."
echo "Base de dades: flaskapp_db"
echo "Usuari: flask_user"
echo "Contrasenya: flask_pass"
echo "================================================="
