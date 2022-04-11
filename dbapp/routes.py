from flask import jsonify, render_template, url_for, flash, redirect, request, abort
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_admin import Admin, AdminIndexView, expose
from flask_bcrypt import Bcrypt
from datetime import datetime

from dbapp import app, db

#Initialize Bycrypt
bcrypt = Bcrypt(app)

from dbapp.models import administrator, agent, buyer, city, commission, house, office, sale, seller
from dbapp.dashboard import *
from dbapp.queries import *

#Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#create login decorator

@login_manager.user_loader
def load_user(id):
    return administrator.Admins.query.get(int(id))

month_year = datetime.utcnow().strftime('%m/%Y')


#custom admin view

class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        data = {
            'top_seller': get_top_seller(),
            'top_agent' : get_top_agent(),
            'top_buyer' : get_top_buyer(),
            'top_office': get_top_office(),
            'summary'   : get_all_listings(),
        }
    
        self._template_args['dashboard'] = (data)
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
    administrator.AdminsView(administrator.Admins, db.session, name='Administrators'),
    agent.AgentsView(agent.Agent, db.session, name='Agents'),
    buyer.BuyersView(buyer.Buyer, db.session, name='Buyers'),
    city.CitiesView(city.City, db.session, name='Cities'),
    commission.CommissionsView(commission.Commission, db.session, name='Commission'),
    seller.SellersView(seller.Seller, db.session, name='Clients'),
    house.HousesView(house.House, db.session, name='Houses'),
    office.OfficesView(office.Office, db.session, name='Offices'),
    sale.SalesView(sale.Sale, db.session, name='Sales'),
)

#login/signup routes

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

#monthly insights

@app.route('/insights/top_5_agents', methods=['POST','GET'])
@login_required
def insights_get_top_5_agents():
    return render_template('insights.html', info_list=get_top_5_agents(), currentMonth=month_year)

@app.route('/insights/top_5_offices', methods=['POST','GET'])
@login_required
def insights_get_top_5_offices():
    return render_template('insights.html', info_list=get_top_5_offices(), currentMonth=month_year)
    
@app.route('/insights/average_house_selling_price', methods=['POST','GET'])
@login_required
def insights_get_avg_selling_price():
    return render_template('insights.html', info_list=get_avg_selling_price(), currentMonth=month_year)

@app.route('/insights/average_house_listing_time', methods=['POST','GET'])
@login_required
def insights_get_avg_listing_time():
    return render_template('insights.html', info_list=get_avg_listing_time(), currentMonth=month_year)


#analytics

@app.route('/analytics/annual_sales', methods=['POST','GET'])
@login_required
def analytics_annual_sales():

    start_date = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
    end_date = datetime(year=2022, month=12, day=31, hour=11, minute=59, second=59)

    raw_data = {}
    processed_data = {'01':0, '02':0, '03':0, '04':0, '05':0, '06':0, '07':0, '08':0, '09':0, '10':0, '11':0, '12':0}
    months = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12 }

    for sold in db.session.query(sale.Sale):
        if sold.date_added >= start_date and sold.date_added <= end_date:
            raw_data[str(sold.date_added.strftime("%d/%m"))] = int(sold.house_price)

    for entry in raw_data:
        month = datetime.strptime(entry,"%d/%m").strftime("%m")
        processed_data[month] += raw_data[entry]

    return render_template('analytics.html', types=['line'], 
                                             titles=['Annual Sales 2022'],
                                             labels= list(months.keys()), 
                                             values=sorted(list(processed_data.values()))
                                             )

#query to generate agents distribution per office
@app.route("/analytics/agents_per_office", methods=["POST", "GET"])
def analytics_agents_offices():

    try:
        all_offices = office.Office.query.all()
        all_offices_info = {}

        # for office_id in range(len(all_offices)+1):
        #     if len(all_offices[office_id].agents_offices) > 0:
        #         all_offices_info[office_id] = len(all_offices[office_id].agents_offices)
        # print(all_offices_info)

        all_offices_info = {a.address: len(
            a.agents_offices) for a in all_offices}

        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Agents Per Office'], 
                                                 labels=sorted(list(all_offices_info.keys())), 
                                                 values=sorted(list(all_offices_info.values()))
                                                 )

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')

#query to generate houses distribution per agent
@app.route("/analytics/houses_per_agent", methods=["POST", "GET"])
def analytics_houses_agents():

    try:
        all_agents = agent.Agent.query.all()
        all_agents_info = {a.lastname: len(a.houses) for a in all_agents}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Properties Per Listing Agent'], 
                                                 labels=sorted(list(all_agents_info.keys())), 
                                                 values=list(all_agents_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate house distribution per city
@app.route("/analytics/houses_per_city", methods=["POST", "GET"])
def analytics_houses_cities():

    try:
        all_cities = city.City.query.all()
        all_cities_info = {a.name: len(a.house_list) for a in all_cities}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Houses Per City'], 
                                                 labels=sorted(list(all_cities_info.keys())), 
                                                 values=list(all_cities_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per price
@app.route("/analytics/houses_per_price", methods=["POST", "GET"])
def analytics_houses_prices():

    try:
        all_houses = house.House.query.all()
        # using int instead of float
        all_houses_info = {int(a.price): a.id for a in all_houses}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Properties Listed Per Price'], 
                                                 labels=sorted(list(all_houses_info.keys())), 
                                                 values=sorted(list(all_houses_info.values())))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per office
@app.route("/analytics/houses_per_office", methods=["POST", "GET"])
def analytics_houses_offices():

    try:
        all_offices = office.Office.query.all()
        all_offices_info = {a.address: len(
            a.house_list) for a in all_offices if len(a.house_list) > 0}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Properties Listed Per Office'], 
                                                 labels=sorted(list(all_offices_info.keys())), 
                                                 values=sorted(list(all_offices_info.values())))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate houses distribution per seller
@app.route("/analytics/houses_per_seller", methods=["POST", "GET"])
def analytics_houses_sellers():

    try:
        all_sellers = seller.Seller.query.all()
        all_sellers_info = {a.lastname: len(a.houses) for a in all_sellers}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Properties Per Owner'], 
                                                 labels=sorted(list(all_sellers_info.keys())), 
                                                 values=list(all_sellers_info.values()))

    except:
        flash('Error! Unable to render data :(', 'error')
        return render_template('analytics.html')


#query to generate office distribution per city
@app.route("/analytics/offices_per_city", methods=["POST", "GET"])
def analytics_offices_cities():

    try:
        all_cities = city.City.query.all()
        all_cities_info = {a.name: len(a.office_list) for a in all_cities}
        return render_template('analytics.html', types=['bar'], 
                                                 titles=['Distribution of Offices Per City'], 
                                                 labels=sorted(list(all_cities_info.keys())), 
                                                 values=list(all_cities_info.values()))

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

    new_admin = administrator.Admins(
        name=name, email=email, password=password1)

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
            flash(
                f"Oops, you put the wrong password, {email}. Try again.", "info")

    else:
        flash(f"{email}, please create an account!", "info")

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "warning")
    return redirect(url_for('index'))