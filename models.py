from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()

def utcnow():
    return datetime.now(pytz.utc)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    backlog_items = db.relationship('BacklogItem', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    lists = db.relationship('GameList', backref='owner', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    platform = db.Column(db.String(64), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    hours_estimated = db.Column(db.Integer)

    reviews = db.relationship('Review', backref='game', lazy=True)
    backlog_items = db.relationship('BacklogItem', backref='game', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    body = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

class BacklogItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False) # planned, playing, finished, dropped
    hours_played = db.Column(db.Float, default=0.0)
    private_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    updated_at = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)

class GameList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)

    items = db.relationship('GameListItem', backref='game_list', lazy=True, cascade="all, delete-orphan")

class GameListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('game_list.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)
    
    game = db.relationship('Game', backref='in_lists')
