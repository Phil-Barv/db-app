from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False) #zipcodes are NOT unique https://www.quora.com/Can-two-cities-share-the-same-ZIP-code
    state = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    #one city can have many offices, but each office can have only one city
    office_list = db.relationship('Office', lazy='select', backref=db.backref('city', lazy='joined'))

    #one city can have many houses, but each house can have only one city
    house_list = db.relationship('House', backref='city', lazy=True)

    def __repr__(self):
        return f'{self.name} {self.zip_code} {self.state}'

class CitiesView(ModelView):
    column_list = ('id','name', 'office_list','house_list', 'zip_code', 'state', 'date_added')
    column_filters = ('name', 'zip_code', 'state', 'date_added')
    column_labels = {'id':'ID','name':'City','office_list': 'Branches', 'house_list': 'Property Listings', 'zip_code': 'Zip', 'state': 'State'}
    column_searchable_list = ['zip_code', 'state']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))