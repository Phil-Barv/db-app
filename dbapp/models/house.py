from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.models.joins import agents_houses, buyers_houses, sellers_houses


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(60), nullable=False)
    bathrooms = db.Column(db.Numeric(11,1), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    sq_footage = db.Column(db.Numeric(11,2), nullable=False)
    price = db.Column(db.Numeric(11,2), nullable=False)
    is_sold = db.Column(db.Boolean, nullable=False, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg') irl we'd have houses' photos and other identifying data

    #one house can have many sales, but each sale can have only one house
    sale_list = db.relationship('Sale', backref='houses', lazy=True)
 
    #many to one relationship to cities and offices
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))

    #many to many relationship to agents, sales and sellers
    agents_houses = db.relationship('Agent', secondary=agents_houses, lazy='subquery',
                                    backref=db.backref('houses', lazy=True))

    buyers_houses = db.relationship('Buyer', secondary=buyers_houses, lazy='subquery',
                                    backref=db.backref('houses', lazy=True))

    sellers_houses = db.relationship('Seller', secondary=sellers_houses, lazy='subquery',
                                    backref=db.backref('houses', lazy=True))
            
    def __repr__(self):
        return f'House {self.id}: {self.address} Price: ${self.price}'

class HousesView(ModelView):
    column_list = ('id', 'address', 'sellers_houses', 'bathrooms', 'bedrooms', 'sq_footage', 'price','is_sold', 'agents_houses', 'sale_list')
    
    column_labels = {'id':'ID', 'sellers_houses':'Owner(s)', 'address':'Property','bathrooms':'Ba', 'is_sold':'Sold',
                    'bedrooms':'Br','sq_footage': 'Sq_ft', 'price': 'Price $', 'agents_houses':' Listing Agent(s)', 
                    'sale_list': 'Property Sales', 'city.name':'City / Name', 'office.address': 'Office / Address', 'date_added': 'Listing Date'}

    column_filters = ('id', 'address', 'bathrooms', 'bedrooms', 'sq_footage', 'price', 'city.name', 'office.address', 
                    'date_added')
                    
    column_searchable_list = ['price']

    #column_default_sort = [('is_sold', True), ('price', True)] #displays sorted view of bought and high price

    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))