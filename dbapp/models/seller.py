from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.routes import bcrypt


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def __repr__(self):
        return f'Seller {self.id}: {self.firstname} {self.lastname}'
        

class SellersView(ModelView):
    column_list = ('id', 'firstname', 'lastname', 'email', 'houses', 'date_added')
    column_filters = ('id', 'firstname', 'lastname', 'email', 'date_added')
    column_labels = {'id':'ID', 'firstname': 'FirstName', 'lastname': 'LastName','houses':'Properties Listed', 'date_added': 'Onboarding Date'}
    column_searchable_list = ['lastname', 'date_added']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))