from dbapp import db
from populate_db.insert import *

if __name__ == "__main__":
    db.create_all()
    create_agents(50)
    create_buyers(100) #number of buyers dictates number of sales
    create_sellers(50) 
    create_cities_and_buildings(50) #enter number of cities only
    create_sales_and_commissions()
    create_admin()

