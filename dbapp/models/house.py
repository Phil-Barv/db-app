from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.models.joins import agents_houses


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(60), nullable=False)
    bathrooms = db.Column(db.Numeric(11,1), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    sq_footage = db.Column(db.Numeric(11,2), nullable=False)
    price = db.Column(db.Numeric(11,2), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #relationships
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))

    #many to many relationship to agents
    agents_houses = db.relationship('Agent', secondary=agents_houses, lazy='subquery',
                                    backref=db.backref('houses', lazy=True))

    #one house can have multiple sales
    sale_list = db.relationship('Sale', backref='house', lazy=True)


    def __repr__(self):
        return f'House {self.id}: {self.address} Price: ${self.price}'


class HousesView(ModelView):
    column_list = ('id', 'seller', 'address', 'bathrooms', 'bedrooms', 'sq_footage', 'price', 'agents_houses', 'city','date_added')
    column_labels = {'id':'ID', 'seller':'Owner','seller.lastname':'Owner / Lastname', 'address':'Property','bathrooms':'Ba', 
                    'bedrooms':'Br','sq_footage': 'Sq_ft', 'price': '$ Price', 'agents_houses':'Assigned Agent(s)', 
                    'date_added': 'Listing Date', 'city.name':'City / Name', 'office.address': 'Office / Address'}

    column_filters = ('id', 'seller.lastname', 'address', 'bathrooms', 'bedrooms', 'sq_footage', 'price', 'city.name', 'office.address', 
                    'date_added')
                    
    column_searchable_list = ['price']
    can_view_details = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))