from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from datetime import datetime
from dbapp import db

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))
    house_price = db.Column(db.Numeric(11, 2), nullable=False)
    comm_amount = db.Column(db.Numeric(11, 2), nullable=False)
    comm_percent = db.Column(db.Numeric(11, 2), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Sale {self.sale_id}: COMM ${self.comm_amount}'

class CommissionsView(ModelView):
    column_list = ('id', 'agent', 'sale', 'house_price', 'comm_percent','comm_amount', 'date_added')
    column_filters = ['id', 'date_added', 'comm_percent', 'house_price']
    column_labels = {'id': 'ID', 'agent': 'Assigned Agent(s)', 'comm_amount': 'COMM $', 'sale':'Sale Details', 
                     'comm_percent':'PER%', 'house_price':'Sale $', 'date_added': 'Sale Date'}
    column_searchable_list = ['date_added']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))