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

3. **Inicialitzar la BD i carregar dades de prova (seed):**
   Aquesta comanda crearà el fitxer `app.db` (en la carpeta `instance/` o directament al directori segons la versió de Flask-SQLAlchemy) i hi inserirà 15 jocs d'exemple.
   ```bash
   flask --app app seed
   ```

4. **Arrancar el servidor:**
   ```bash
   flask --app app run --debug
   ```

5. Obre el navegador a `http://127.0.0.1:5000/`.

---

## 5 proves manuals (Checklist)

- [ ] **1. Registre + login:**
  Ves a "Registrar-se", crea un compte (per exemple: `usuari1`, `test@test.com`, `12345678`). Un cop registrat, la plataforma et redirigirà a Iniciar sessió. Entra amb el teu email i contrasenya.

- [ ] **2. Buscar joc al catàleg:**
  Ves a la pestanya "Catàleg" i fes servir el camp de text o els desplegables per filtrar per nom (ex: "Zelda"), plataforma ("PC") o gènere ("RPG").

- [ ] **3. Afegir joc al backlog i canviar estat:**
  Dins del catàleg o la fitxa del joc, clica a "+ Afegir al Backlog". Defineix el teu estat inicial (ex: "Planejat"), les hores jugades i desat. Després ves a "El meu Backlog" o al teu Dashboard i clica a "Editar" per canviar l'estat a "Jugant".

- [ ] **4. Crear ressenya pública i veure-la a la fitxa:**
  Entra a la fitxa d'un joc que hagis jugat, clica a "Escriure ressenya". Posa-li una nota (1-5), escriu un text i deixa marcat "Fer pública aquesta ressenya". Al tornar a la fitxa del joc, veuràs la ressenya a l'apartat "Ressenyes de la comunitat".

- [ ] **5. Fer ressenya privada:**
  Canvia la teva ressenya anterior o escriu-ne una de nova desmarcant la casella "Fer pública...". Accedeix al catàleg sense iniciar sessió (fent Logout) i comprova que la ressenya NO apareix a la fitxa del joc per als altres usuaris.