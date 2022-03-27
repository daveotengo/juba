import os
from time import time

import jwt
from flask import Blueprint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.constants import ACCESS
from app import db



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer)
    register_date = db.Column(db.DateTime())


    def __init__(self, name, email, username, register_date,access=ACCESS['guest']):
        #self.id = ''
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = ''
        self.access = access
        self.register_date = register_date

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_user(self):
        return self.access == ACCESS['user']

    def allowed(self, access_level):
        return self.access >= access_level

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.email)



    def get_reset_token(self, expires=500):
        return jwt.encode(
            {'reset_password': self.email, 'exp': time() + expires},
            os.getenv('SECRET_KEY', 'random_key'), algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            email = jwt.decode(token, os.getenv('SECRET_KEY', 'random_key'),
                                  algorithms='HS256')['reset_password']
            print("printing decoded email")
            print(email)
        except:
            return
        print("printing decoded email")
        print(email)
        return User.query.filter_by(email=email).first()

    @staticmethod
    def verify_email(email):
        user = User.query.filter_by(email=email).first()
        return user