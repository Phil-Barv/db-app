from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from dbapp import db

agents_offices = db.Table('agents_offices', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('office_id', db.Integer, db.ForeignKey('office.id'))
)

agents_houses = db.Table('agents_houses', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
)

agents_sales = db.Table('agents_sales', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'))
)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'Agent {self.id}: {self.firstname} {self.lastname}'

class AgentsView(ModelView):
    column_list = ('id', 'firstname', 'lastname', 'email', 'date_added')
    column_filters = ('id', 'firstname', 'lastname', 'email', 'date_added')
    column_labels = {'id':'ID', 'firstname': 'First Name', 'lastname': 'Last Name', 'date_added': 'Start Date'}
    column_searchable_list = ['lastname', 'date_added']



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
    column_list = ('name', 'office_list','house_list', 'zip_code', 'state', 'date_added')
    column_filters = ('name', 'zip_code', 'state', 'date_added')
    column_labels = {'name':'City','office_list': 'Branches', 'house_list': 'Property Listings', 'zip_code': 'Zip', 'state': 'State'}
    column_searchable_list = ['zip_code', 'state']



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
    column_list = ('id', 'seller', 'address', 'bathrooms', 'bedrooms', 'sq_footage', 'price', 'agents_houses', 'date_added')
    column_labels = {'id':'ID', 'seller':'Owner','seller.lastname':'Owner / Lastname', 'bathrooms':'Baths','sq_footage': 'Sq_ft',
                    'agents_houses':'Assigned Agent(s)', 'date_added': 'Listing Date', 'city.name':'City / Name', 'office.address': 'Office / Address'}
    column_filters = ('id', 'seller.lastname', 'address', 'bathrooms', 'bedrooms', 'sq_footage', 'price', 'city.name', 'office.address', 'date_added')
    column_searchable_list = ['price']
    can_view_details = True
    edit_modal = True


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
    column_labels = {'id':'ID', 'firstname': 'First Name', 'lastname': 'Last Name', 'house_list':'Properties Listed', 'date_added': 'Start Date'}
    column_searchable_list = ['lastname', 'date_added']


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
