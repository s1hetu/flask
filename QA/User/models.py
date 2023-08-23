import app
from QA import db
from flask import current_app
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String, default="ac")

    def __repr__(self):
        return f"User : {self.username}"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='tags', lazy=True)

    def __repr__(self):
        return self.name


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', uselist=False, backref='address', lazy=True)

    def __repr__(self):
        return f"{self.user}-{self.city}"
