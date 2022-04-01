from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #one seller can have many houses, but each house can have only one seller -> assumes NO co-owning property
    house_list = db.relationship('House', backref='seller', lazy=True)


    def __repr__(self):
        return f'Seller {self.id}: {self.firstname} {self.lastname}'
        

class SellersView(ModelView):
    column_list = ('id', 'firstname', 'lastname', 'email', 'house_list', 'date_added')
    column_filters = ('id', 'firstname', 'lastname', 'email', 'date_added')
    column_labels = {'id':'ID', 'firstname': 'First Name', 'lastname': 'Last Name', 'house_list':'Properties Listed', 'date_added': 'Onboarding Date'}
    column_searchable_list = ['lastname', 'date_added']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))