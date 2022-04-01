from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.models.joins import agents_sales


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #many to many relationship to agents
    agents_sales = db.relationship('Agent', secondary=agents_sales, lazy='subquery',
                                    backref=db.backref('sales', lazy=True))

    def __repr__(self):
        return f'Sale by: {self.agents_sales} House: {self.house_id}'

class SalesView(ModelView):
    column_list = ('id', 'house', 'agents_sales', 'date_added')
    column_filters = ('id', 'house', 'agents_sales', 'date_added')
    column_labels = {'id':'ID', 'house': 'Property Details', 'agents_sales': 'Sold By', 'date_added': 'Sale Date'}
    column_searchable_list = ['date_added']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))