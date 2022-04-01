from flask import jsonify, render_template, url_for, flash, redirect, request, abort
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_admin import Admin, AdminIndexView, expose
from flask_bcrypt import Bcrypt

from dbapp import app, db
from dbapp.models import administrator, agent, city, house, office, sale, seller

#Initialize Bycrypt
bcrypt = Bcrypt(app)

#Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#create login decorator
@login_manager.user_loader
def load_user(id):
    return administrator.Admins.query.get(int(id))


class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(CustomAdminIndexView, self).index()

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash('Please sign in to access this page!')
        return redirect(url_for('login'))


#create admin instance
admin = Admin(app, name="Dunder Mifflin Realtors", template_mode='bootstrap4', index_view=CustomAdminIndexView(
    name="Dashboard", menu_icon_type="fa", menu_icon_value="fa-dashboard"))

#add data views
admin.add_views(
    administrator.AdminsView(administrator.Admins, db.session, name='Administators'),
    agent.AgentsView(agent.Agent, db.session, name='Agents'),
    city.CitiesView(city.City, db.session, name='Cities'),
    house.HousesView(house.House, db.session, name='Houses'),
    office.OfficesView(office.Office, db.session, name='Offices'),
    sale.SalesView(sale.Sale, db.session, name='Sales'),
    seller.SellersView(seller.Seller, db.session, name='Sellers'),
)

from random import sample 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/analytics/')
@login_required
def analytics():
    
    data = [
        ("01-01-2022", 1597),
        ("02-01-2022", 1456),
        ("03-01-2022", 1908),
        ("04-01-2022", 896),
        ("05-01-2022", 755),
        ("06-01-2022", 453),
        ("07-01-2022", 1100),
        ("08-01-2022", 1235),
        ("09-01-2022", 1478),
    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template('analytics.html', types=['line'], titles=['Test Data Samples'], labels=labels, values=values)


#query to generate agents distribution per office
@app.route("/analytics/agents_per_office", methods=["POST", "GET"])
def analytics_agents_offices():

    try:
        all_offices = office.Office.query.all()
        all_offices_info= {a.address:len(a.agents_offices) for a in all_offices}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Agents Per Office'], labels=list(all_offices_info.keys()), values=list(all_offices_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')

#query to generate houses distribution per agent
@app.route("/analytics/houses_per_agent", methods=["POST", "GET"])
def analytics_houses_agents():

    try:
        all_agents = agent.Agent.query.all()
        all_agents_info= {a.lastname:len(a.houses) for a in all_agents}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Properties Per Listing Agent'], labels=list(all_agents_info.keys()), values=list(all_agents_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate house distribution per city
@app.route("/analytics/houses_per_city", methods=["POST", "GET"])
def analytics_houses_cities():

    try:
        all_cities = city.City.query.all()
        all_cities_info= {a.name:len(a.house_list) for a in all_cities}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Houses Per City'], labels=list(all_cities_info.keys()), values=list(all_cities_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per price
@app.route("/analytics/houses_per_price", methods=["POST", "GET"])
def analytics_houses_prices():

    try:
        all_houses = house.House.query.all()
        all_houses_info= {int(a.price):a.id for a in all_houses} #using int instead of float
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Properties Listed Per Price'], labels=list(all_houses_info.keys()), values=list(all_houses_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per office
@app.route("/analytics/houses_per_office", methods=["POST", "GET"])
def analytics_houses_offices():

    try:
        all_offices = office.Office.query.all()
        all_offices_info= {a.address:len(a.house_list) for a in all_offices}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Properties Listed Per Office'], labels=list(all_offices_info.keys()), values=list(all_offices_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per seller
@app.route("/analytics/houses_per_seller", methods=["POST", "GET"])
def analytics_houses_sellers():

    try:
        all_sellers = seller.Seller.query.all()
        all_sellers_info= {a.lastname:len(a.house_list) for a in all_sellers}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Properties Per Owner'], labels=list(all_sellers_info.keys()), values=list(all_sellers_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate office distribution per city
@app.route("/analytics/offices_per_city", methods=["POST", "GET"])
def analytics_offices_cities():

    try:
        all_cities = city.City.query.all()
        all_cities_info= {a.name:len(a.office_list) for a in all_cities}
        return render_template('analytics.html', types=['bar'], titles=['Distribution of Offices Per City'], labels=list(all_cities_info.keys()), values=list(all_cities_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password2 != password1:
        flash('The two password fields does not match')
        return redirect(url_for('signup'))

    if administrator.Admins.query.filter_by(name=name).first():
        flash('Username address already exists')
        return redirect(url_for('signup'))

    if administrator.Admins.query.filter_by(email=email).first():
        flash('Email address already exists')
        return redirect(url_for('signup'))

    hashed_password = bcrypt.generate_password_hash(password1)
    new_admin = administrator.Admins(name=name, email=email, password=hashed_password)

    db.session.add(new_admin)
    db.session.commit()
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    admin = administrator.Admins.query.filter_by(email=email).first()

    if admin == None:
        flash('Please create an account to log in.', 'info')
        return redirect(url_for('login'))

    if admin:
        if bcrypt.check_password_hash(admin.password, password):
            login_user(admin, remember=remember)
            return redirect(url_for('admin.index'))

        else:
            flash(f"Oops, you put the wrong password, {email}. Try again.", "info") 

    else:
        flash(f"{email}, please create an account!", "info")
    
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "warning")
    return redirect(url_for('index'))