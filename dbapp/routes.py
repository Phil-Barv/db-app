from flask import render_template, url_for, flash, redirect, request, abort
from flask_bcrypt import Bcrypt
from flask_admin.contrib.sqla import ModelView

from datetime import datetime, timedelta
from dbapp import app, db, admin

from dbapp.forms import TaskForm, AgentForm
from dbapp.models import *


#Initialize Bycrypt
bcrypt = Bcrypt(app)

# #define default views
# view1 = {"title": "Username", "t_link": "home", "function": "Log Out", "f_link": "logout", "dialog":"Are you sure you want to log out?" }
# view2 = {"title": "Sign Up", "t_link": "signup", "function": "Log In", "f_link": "login", "dialog":"Please enter your credentials below!" }
# view3 = {"title": "Take me back", "t_link": "home", "function": "Home", "f_link": "home", "dialog":"You are going to be redirected!" }
# view4 = {"title": "Take me back", "t_link": "new", "function": "Home", "f_link": "new", "dialog":"You are going to be redirected!" }

# @app.route('/', methods = ["GET", "POST"])
# @app.route('/home/', methods = ["GET", "POST"])
# def home():
#     #calculate today and yesterday for task timestamp formatting
#     today = datetime.utcnow().date()
#     yesterday = today - timedelta(hours=24)

#     agents = Agent.query.all()
#     return render_template('home.html', view=view4, task_list=agents, today=today, yesterday=yesterday)

# @app.route('/new/', methods = ["GET", "POST"])
# def new():

#     form = AgentForm()

#     if request.method == "POST":
#         hashed_password = bcrypt.generate_password_hash(form.password.data)

#         new_agent = Agent(
#             firstname = form.firstname.data,
#             lastname = form.lastname.data,
#             email = form.email.data,
#             password = hashed_password
#             )

#         try:
#             db.session.add(new_agent)
#             db.session.commit()
#             flash("Your account has been added, Sign In!", "info")
#             return redirect(url_for('home'))

#         except:
#             abort(500)

#     return render_template('new.html', view=view4, form=form)

#add admin
admin.add_views(
    AgentsView(Agent, db.session, name='Agents'),
    HousesView(House, db.session, name='Houses'),
    OfficesView(Office, db.session, name='Offices'),
    SalesView(Sale, db.session, name='Sales'),
    CitiesView(City, db.session, name='Cities'),
)
