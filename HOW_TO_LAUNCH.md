# Guia de llançament de GameBacklog (Flask)

Aquest document explica pas a pas com configurar l'entorn de base de dades i de Python per posar en marxa l'aplicació web. 

L'aplicació utilitza **Python 3.8+** (amb Flask) i **MySQL** per a la base de dades.

## 1. Configuració de la Base de Dades (MySQL)

L'aplicació depèn d'un servidor MySQL actiu amb una base de dades anomenada `flaskapp_db` i un usuari predeterminat. Per sort, s'ha creat un script bash automatitzat que ho prepara.

1. Dona permisos d'execució a l'script d'instal·lació de la base de dades:
   ```bash
   chmod +x scripts/setup_db.sh
   ```

2. Executa l'script de configuració. Aquest script instal·larà `mysql-server` (si no el tens), establirà els usuaris necessaris i farà un bolcat inicial opcional de dades:
   ```bash
   ./scripts/setup_db.sh
   ```
   *(Nota: Se't pot demanar la contrasenya de sudo/root del teu sistema operatiu o de MySQL)*

## 2. Configuració de l'Entorn de Python

Sempre és recomanable usar un entorn virtual (`venv`) per a les dependències de Python de forma aïllada del sistema.

1. **Crear l'entorn virtual (venv):**
   Situa't a l'arrel del projecte (on es troba `app.py`) i executa:
   ```bash
   python3 -m venv venv
   ```

2. **Activar l'entorn virtual:**
   - A Linux/Ubuntu/MacOS:
     ```bash
     source venv/bin/activate
     ```
   - A Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Instal·lar les dependències requerides:**
   Un cop activat el `venv`, instal·la totes les llibreries que demana Flask (inclòs SQLAlchemy, PyMySQL i Werkzeug):
   ```bash
   pip install -r requirements.txt
   ```

> [!WARNING]
> **Problemes freqüents a WSL (Windows Subsystem for Linux):**
> Si en provar d'executar `pip install` o `python3` la teva terminal es queda totalment "penjada" (congelada) sense donar cap error, és possible que l'entorn virtual no s'hagi lligat bé amb els executables de Python del sistema rutinari.
> **Solució:** Esborra la carpeta `venv` completament (`rm -rf venv`) i torna-la a crear i activar pas a pas manualment tal i com s'indica a dalt. Assegurat d'estar corrent les comandes directament en un terminal interactiu i no dins de processos en segon plà (background).

## 3. Població Inicial de la BD (opcional)

Tot i que l'script `setup_db.sh` carrega dades de l'arxiu `sql/db.sql` o `scripts/db.sql` si existeixen, el propi Flask té una comanda integrada per recrear les taules per defecte i afegir 15 jocs d'exemple si calgués.

Per poblar de jocs inicials la teva BD local:
```bash
flask --app app seed
```
*(Això netejarà qualsevol joc existent i en crearà 15 de nous a la BD)*

## 4. Llançar el Servidor de Desenvolupament

Quan l'entorn i la base de dades estiguin a punt, només queda arrencar l'aplicació Flask.

1. Executa la següent comanda:
   ```bash
   flask --app app run --debug
   ```
   *(L'opció `--debug` permet que el servidor es reiniciï sol en detectar canvis al codi)*

2. Obre el teu navegador a: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

I ja hauries de veure la pàgina de la botiga / gestor de backlog funcionant al teu equip local de forma correcta!
