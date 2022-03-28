from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)

app.secret_key = "VerySecretKey" #change before deployment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #removes modifications to database warnings

# set bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'yeti'

#create db instance
db = SQLAlchemy(app)

#create admin instance
admin = Admin(app, name="Dunder Mifflin Realtors", template_mode='bootstrap4')

#import routes after creating app and db to prevent circular import
from dbapp import routes