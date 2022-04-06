from dbapp import db

agents_offices = db.Table('agents_offices', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('office_id', db.Integer, db.ForeignKey('office.id'))
)

agents_houses = db.Table('agents_houses', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
)

buyers_houses = db.Table('buyers_houses', 
    db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id')),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
)

buyers_sales = db.Table('buyers_sales', 
    db.Column('buyer_id', db.Integer, db.ForeignKey('buyer.id')),
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'))
)

sellers_houses = db.Table('sellers_houses', 
    db.Column('seller_id', db.Integer, db.ForeignKey('seller.id')),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'))
)

agents_sales = db.Table('agents_sales', 
    db.Column('agent_id', db.Integer, db.ForeignKey('agent.id')),
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'))
)