from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.models.joins import agents_sales, buyers_sales


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    #one sale can have many commissions depending on no. of listing agents, but each individual commission can have only one sale
    commission_list = db.relationship('Commission', lazy='select', backref=db.backref('sale', lazy='joined'))
    house_price = db.Column(db.Numeric(11, 2), nullable=False, index=True)

    #many to many relationship to agents
    agents_sales = db.relationship('Agent', secondary=agents_sales, lazy='subquery',
                                    backref=db.backref('sales', lazy=True))

    buyers_sales = db.relationship('Buyer', secondary=buyers_sales, lazy='subquery',
                                backref=db.backref('sales', lazy=True))

    def __repr__(self):
        return f'Sale {self.id} bought House {self.house_id}'


class SalesView(ModelView):
    column_list = ('id', 'buyers_sales', 'houses', 'agents_sales', 'commission_list', 'date_added')
    column_filters = ('id', 'agents_sales', 'date_added')

    column_labels = {'id':'ID', 'buyers_sales':'Buyer(s)', 'houses': 'Property Details', 'agents_sales': 'Assigned Agent(s)', 
                     'commission_list':'Commission(s)', 'date_added': 'Sale Date'}

    column_searchable_list = ['date_added']

    column_default_sort = [('date_added', True)] #displays sorted view of bought and high price

    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))