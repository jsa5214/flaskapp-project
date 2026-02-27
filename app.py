import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from models import db, User, Game, Review, BacklogItem, GameList, GameListItem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:flask_pass@localhost/flaskapp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Si us plau, inicia sessió per accedir a aquesta pàgina."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- PUBLIC ROUTES ---

@app.route('/')
def index():
    # Buscador rápido q=? ...
    q = request.args.get('q', '').strip()
    if q:
        return redirect(url_for('games', q=q))
    
    # Top 5 games by avg rating
    top_games = db.session.query(
        Game, func.avg(Review.rating).label('avg_rating')
    ).join(Review).filter(Review.is_public == True)\
    .group_by(Game.id).order_by(db.desc('avg_rating')).limit(5).all()
    
    # Latest public reviews
    latest_reviews = Review.query.filter_by(is_public=True).order_by(Review.created_at.desc()).limit(5).all()
    
    return render_template('index.html', top_games=top_games, latest_reviews=latest_reviews)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/games')
def games():
    q = request.args.get('q', '').strip()
    platform = request.args.get('platform', '')
    genre = request.args.get('genre', '')
    
    query = Game.query
    if q:
        query = query.filter(Game.title.ilike(f'%{q}%'))
    if platform:
        query = query.filter_by(platform=platform)
    if genre:
        query = query.filter_by(genre=genre)
        
    games_list = query.all()
    
    # filters for UI
    platforms = db.session.query(Game.platform).distinct().all()
    genres = db.session.query(Game.genre).distinct().all()
    
    return render_template('games.html', games=games_list, 
                           platforms=[p[0] for p in platforms], 
                           genres=[g[0] for g in genres],
                           current_p=platform, current_g=genre, current_q=q)

@app.route('/games/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    public_reviews = Review.query.filter_by(game_id=game.id, is_public=True).order_by(Review.created_at.desc()).all()
    
    avg_rating = db.session.query(func.avg(Review.rating)).filter_by(game_id=game.id, is_public=True).scalar()
    
    user_backlog_item = None
    user_review = None
    if current_user.is_authenticated:
        user_backlog_item = BacklogItem.query.filter_by(user_id=current_user.id, game_id=game.id).first()
        user_review = Review.query.filter_by(user_id=current_user.id, game_id=game.id).first()
        
    return render_template('game_detail.html', game=game, reviews=public_reviews, 
                           avg_rating=avg_rating, backlog_item=user_backlog_item, user_review=user_review)


# --- AUTHENTICATION ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash("Les contrasenyes no coincideixen.", "danger")
            return redirect(url_for('register'))
            
        if len(password) < 8:
            flash("La contrasenya ha de tenir almenys 8 caràcters.", "danger")
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash("El correu electrònic ja està registrat.", "danger")
            return redirect(url_for('register'))
            
        if User.query.filter_by(username=username).first():
            flash("El nom d'usuari ja existeix.", "danger")
            return redirect(url_for('register'))
            
        user = User(
            username=username, 
            email=email, 
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash("Compte creat correctament! Ara pots iniciar sessió.", "success")
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Sessió iniciada correctament.", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
            
        flash("Correu electrònic o contrasenya incorrectes.", "danger")
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has tancat la sessió correctament.", "success")
    return redirect(url_for('index'))


# --- PRIVATE ROUTES ---

@app.route('/dashboard')
@login_required
def dashboard():
    backlog_counts = {
        'planned': BacklogItem.query.filter_by(user_id=current_user.id, status='planned').count(),
        'playing': BacklogItem.query.filter_by(user_id=current_user.id, status='playing').count(),
        'finished': BacklogItem.query.filter_by(user_id=current_user.id, status='finished').count(),
        'dropped': BacklogItem.query.filter_by(user_id=current_user.id, status='dropped').count()
    }
    
    latest_updates = BacklogItem.query.filter_by(user_id=current_user.id).order_by(BacklogItem.updated_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', counts=backlog_counts, latest_updates=latest_updates)

@app.route('/backlog')
@login_required
def backlog():
    status_filter = request.args.get('status')
    query = BacklogItem.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    items = query.order_by(BacklogItem.updated_at.desc()).all()
    return render_template('backlog.html', items=items, current_status=status_filter)

@app.route('/backlog/add/<int:game_id>', methods=['GET', 'POST'])
@login_required
def backlog_add(game_id):
    game = Game.query.get_or_404(game_id)
    item = BacklogItem.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    
    if request.method == 'POST':
        status = request.form.get('status')
        hours = float(request.form.get('hours_played', 0))
        note = request.form.get('private_note', '')
        
        if item:
            item.status = status
            item.hours_played = hours
            item.private_note = note
            flash("Estat del joc actualitzat.", "success")
        else:
            item = BacklogItem(user_id=current_user.id, game_id=game.id, status=status, hours_played=hours, private_note=note)
            db.session.add(item)
            flash("Joc afegit al teu backlog.", "success")
            
        db.session.commit()
        return redirect(url_for('backlog'))
        
    return render_template('backlog_form.html', game=game, item=item)

@app.route('/reviews/new/<int:game_id>', methods=['GET', 'POST'])
@login_required
def review_form(game_id):
    game = Game.query.get_or_404(game_id)
    review = Review.query.filter_by(user_id=current_user.id, game_id=game.id).first()
    
    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        body = request.form.get('body')
        is_public = 'is_public' in request.form
        
        if review:
            review.rating = rating
            review.body = body
            review.is_public = is_public
            flash("Resenya actualitzada.", "success")
        else:
            review = Review(user_id=current_user.id, game_id=game.id, rating=rating, body=body, is_public=is_public)
            db.session.add(review)
            flash("Resenya publicada.", "success")
            
        db.session.commit()
        return redirect(url_for('game_detail', game_id=game.id))
        
    return render_template('review_form.html', game=game, review=review)

@app.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def review_delete(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        abort(403)
        
    game_id = review.game_id
    db.session.delete(review)
    db.session.commit()
    flash("Resenya eliminada.", "success")
    return redirect(url_for('game_detail', game_id=game_id))

@app.route('/lists', methods=['GET', 'POST'])
@login_required
def lists():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            new_list = GameList(user_id=current_user.id, name=name, description=description)
            db.session.add(new_list)
            db.session.commit()
            flash("Llista creada.", "success")
            return redirect(url_for('lists'))
            
    user_lists = GameList.query.filter_by(user_id=current_user.id).all()
    return render_template('lists.html', lists=user_lists)

@app.route('/lists/<int:list_id>', methods=['GET', 'POST'])
@login_required
def list_detail(list_id):
    glist = GameList.query.get_or_404(list_id)
    if glist.user_id != current_user.id:
        abort(403)
        
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            game_id = request.form.get('game_id')
            if game_id and not GameListItem.query.filter_by(list_id=glist.id, game_id=game_id).first():
                item = GameListItem(list_id=glist.id, game_id=game_id)
                db.session.add(item)
                db.session.commit()
                flash("Joc afegit a la llista.", "success")
        elif action == 'remove':
            item_id = request.form.get('item_id')
            item = GameListItem.query.get(item_id)
            if item and item.list_id == glist.id:
                db.session.delete(item)
                db.session.commit()
                flash("Joc eliminat de la llista.", "success")
                
        return redirect(url_for('list_detail', list_id=list_id))
        
    available_games = Game.query.all()
    return render_template('list_detail.html', glist=glist, available_games=available_games)


# --- ERROR HANDLERS ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# --- SEED COMMAND ---
@app.cli.command("seed")
def seed_data():
    """Seed the database with sample games."""
    db.drop_all()
    db.create_all()
    
    # 15 sample games
    games_data = [
        {"title": "The Legend of Zelda: Breath of the Wild", "platform": "Nintendo Switch", "genre": "Action-Adventure", "year": 2017, "description": "Step into a world of discovery, exploration, and adventure.", "hours_estimated": 50},
        {"title": "The Witcher 3: Wild Hunt", "platform": "PC", "genre": "RPG", "year": 2015, "description": "As war rages on throughout the Northern Realms, you take on the greatest contract of your life.", "hours_estimated": 100},
        {"title": "Red Dead Redemption 2", "platform": "PS4", "genre": "Action-Adventure", "year": 2018, "description": "Arthur Morgan and the Van der Linde gang are outlaws on the run.", "hours_estimated": 60},
        {"title": "Super Mario Odyssey", "platform": "Nintendo Switch", "genre": "Platformer", "year": 2017, "description": "Explore incredible places far from the Mushroom Kingdom.", "hours_estimated": 15},
        {"title": "Minecraft", "platform": "PC", "genre": "Sandbox", "year": 2011, "description": "Prepare for an adventure of limitless possibilities as you build, mine, battle mobs, and explore.", "hours_estimated": 200},
        {"title": "Hollow Knight", "platform": "PC", "genre": "Metroidvania", "year": 2017, "description": "Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.", "hours_estimated": 30},
        {"title": "Bloodborne", "platform": "PS4", "genre": "Action RPG", "year": 2015, "description": "Hunt your nightmares as you search for answers in the ancient city of Yharnam.", "hours_estimated": 40},
        {"title": "Persona 5 Royal", "platform": "PS4", "genre": "JRPG", "year": 2019, "description": "Don the mask of Joker and join the Phantom Thieves of Hearts.", "hours_estimated": 110},
        {"title": "God of War", "platform": "PS4", "genre": "Action-Adventure", "year": 2018, "description": "His vengeance against the Gods of Olympus years behind him, Kratos now lives as a man in the realm of Norse Gods.", "hours_estimated": 25},
        {"title": "Elden Ring", "platform": "PC", "genre": "Action RPG", "year": 2022, "description": "Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring.", "hours_estimated": 80},
        {"title": "Tetris Effect", "platform": "PC", "genre": "Puzzle", "year": 2018, "description": "Tetris like you've never seen it, or heard it, or felt it before.", "hours_estimated": 10},
        {"title": "Hades", "platform": "PC", "genre": "Roguelike", "year": 2020, "description": "Defy the god of the dead as you hack and slash out of the Underworld.", "hours_estimated": 25},
        {"title": "Super Smash Bros. Ultimate", "platform": "Nintendo Switch", "genre": "Fighting", "year": 2018, "description": "Legendary game worlds and fighters collide in the ultimate showdown.", "hours_estimated": 50},
        {"title": "Celeste", "platform": "PC", "genre": "Platformer", "year": 2018, "description": "Help Madeline survive her inner demons on her journey to the top of Celeste Mountain.", "hours_estimated": 12},
        {"title": "Stardew Valley", "platform": "PC", "genre": "Simulation", "year": 2016, "description": "You've inherited your grandfather's old farm plot in Stardew Valley.", "hours_estimated": 150}
    ]
    
    for gdata in games_data:
        game = Game(**gdata)
        db.session.add(game)
        
    db.session.commit()
    print(f"Seed completed: {len(games_data)} games added.")

if __name__ == '__main__':
    app.run(debug=True)
