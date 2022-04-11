from dbapp import db
from populate_db.insert import *

def populate_db_for_test():
    """
    Function used in populating test db
    """
    #numbers reduced as data is created and destroyed several times.
    create_agents(20)
    create_buyers(60) 
    create_sellers(30) 
    create_cities_and_buildings(20)
    create_sales_and_commissions()
    create_admin()


if __name__ == "__main__":
    db.create_all()
    create_agents(50)
    create_buyers(100) #number of buyers dictates number of sales
    create_sellers(50) 
    create_cities_and_buildings(50) #enter number of cities only
    create_sales_and_commissions()
    create_admin()

