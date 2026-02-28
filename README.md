# GameBacklog

Aplicació web en Python (Flask) per gestionar un "backlog" de videojocs (catàleg, estat de joc, ressenyes, llistes).

## Requisits

- Python 3.8+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Login 0.6.3
- Werkzeug 3.0.1
- pytz 2024.1

## Passos per a l'execució

1. **Crear l'entorn virtual (opcional però recomanat):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # A Linux/Mac
   venv\Scripts\activate     # A Windows
   ```

2. **Instal·lar les dependències:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicialitzar la BD (MySQL) i carregar dades de prova (seed):**
   L'aplicació utilitza MySQL en lloc de SQLite. Abans de poblar la base de dades des de Flask, has de configurar el servidor MySQL i crear els usuaris necessaris utilitzant l'script automatitzat:
   ```bash
   chmod +x scripts/setup_db.sh
   ./scripts/setup_db.sh
   ```
   *(Aquest script et demanarà permissos d'administrador per instal·lar i configurar MySQL al teu equip)*
   
   Un cop la base de dades estigui creada, pots inserir els 15 jocs d'exemple del catàleg mitjançant Flask:
   ```bash
   flask --app app seed
   ```

4. **Arrancar el servidor:**
   ```bash
   flask --app app run --debug
   ```

5. Obre el navegador a `http://127.0.0.1:5000/`.

