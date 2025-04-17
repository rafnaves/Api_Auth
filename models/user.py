from database import db

from flask_login import UserMixin

class User(db.Model, UserMixin):
    #id (int), username (text), password (text), role (text)
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable = False)
    role = db.Column(db.String(80), nullable = False, default='user')

class Meal(db.Model, UserMixin):
    # Nome (text), Descrição (text), Data/hora (date), Dentro da dieta? (boolean)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    dentro_da_dieta = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('meals', lazy=True))

