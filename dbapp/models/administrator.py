from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from datetime import datetime
from dbapp import db

#created this unnecessary class cause I didn't want to delete my login and signup forms 
class Admins(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Admin {self.id}: {self.name}'

class AdminsView(ModelView):
    column_list = ('id', 'name', 'email', 'date_added')
    column_filters = ('id', 'name', 'date_added')
    column_labels = {'id':'ID', 'name': 'Admin Name', 'date_added': 'Date Onboarded'}
    column_searchable_list = ['date_added']

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))