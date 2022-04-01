from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user
from datetime import datetime
from dbapp import db
from dbapp.models.joins import agents_offices

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    #one office can have many houses, but each house can have only one office
    house_list = db.relationship('House', backref='office', lazy=True)

    #many to many relationship to agents
    agents_offices = db.relationship('Agent', secondary=agents_offices, lazy='subquery',
                                    backref=db.backref('offices', lazy=True))

    def __repr__(self):
        return f'Office {self.id}: {self.address}'

class OfficesView(ModelView):
    column_list = ('id', 'address', 'agents_offices', 'house_list', 'city', 'date_added')
    column_filters = ('id', 'address','agents_offices.lastname','city.name', 'city.state', 'date_added')
    column_labels = {'id': 'ID', 'address': 'Branch', 'agents_offices.lastname':'Agents / Lastname',
                    'agents_offices':'Available Agents','house_list':'Listed Properties', 'city':'City Address',
                    'city.name':'City / Name', 'city.state':'City / State','date_added': 'Date Opened'}
    column_searchable_list = ['address']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
