from dbapp import app, db
import dbapp
from dbapp import app, db
from dbapp.models import Agent, House, Office, Sale, City, Seller

import names
from uszipcode import SearchEngine
import geonamescache
from random import sample, randint, uniform

def create_agents(agents):

    for _ in range(agents):
        firstname = names.get_first_name()
        lastname = names.get_last_name()
        email = f"{firstname.lower()}.{lastname.lower()}@mifflin.com"
        
        #generic password for all test agents
        password = "Fizz"

        #check if agent already exists before adding them -> maintain unique users for testing
        agent_exists = Agent.query.filter_by(email=email).first()

        if agent_exists == None:
            db.session.add(Agent(firstname=firstname, lastname=lastname, email=email, password=password))
    
    #commit as a single transaction
    db.session.commit()


def create_sellers(sellers):
    
    for _ in range(sellers):
        firstname = names.get_first_name()
        lastname = names.get_last_name()
        email = f"{firstname.lower()}.{lastname.lower()}@gmail.com"
        
        #generic password for all test sellers
        password = "Buzz"

        #check if seller already exists before adding them -> names may overlap with agents but emails are unique
        seller_exists = Seller.query.filter_by(email=email).first()

        if seller_exists == None:
            db.session.add(Seller(firstname=firstname, lastname=lastname, email=email, password=password))
    
    #commit as a single transaction
    db.session.commit()


def create_cities_and_buildings(cities):
    gc = geonamescache.GeonamesCache()
    sr = SearchEngine()

    c = gc.get_cities()
    s = gc.get_us_states_by_names()

    all_states = {s[key]['code']:s[key]['name'] for key in list(s.keys())}
    all_cities = [c[key]['name'] for key in list(c.keys()) if c[key]['countrycode'] == 'US']
    
    sample_cities = sample(all_cities, cities) #remove duplicates if any

    agents = Agent.query.all()
    office_id = 0

    print('\nGenerating City, Office and House Data. This might take a while...\n')

    for city_id in range(len(sample_cities)):
        zipcodes = sr.by_city(city=sample_cities[city_id])
        try:
            print('CITY', zipcodes[0].major_city, zipcodes[0].zipcode, all_states[zipcodes[0].state])
            db.session.add(City(name=zipcodes[0].major_city, zip_code=zipcodes[0].zipcode, state=all_states[zipcodes[0].state]))
        except:
            continue

        for building in zipcodes:
            sample_office_agents = sample(agents, 5)
            city_address = f'{sample_cities[city_id]} {building.zipcode} {all_states[building.state]}'

            #unique cities guaranteed by sampling without replacement
            print('OFFICE', sample_cities[city_id], building.zipcode, all_states[building.state], sample_office_agents)
            db.session.add(Office(address = city_address, city_id = city_id, agents_offices = sample_office_agents))

            #give each house a surname as its fictitious address
            house_address = f'{names.get_last_name()}, {city_address}'
            guess = uniform(0, 1)
            if guess <= 0.1: 
                guess = 0.05

            #round to .5 as you can have .5 baths in real estate
            bathrooms = round(guess*20)*0.5
            
            #assume ratio of 1.8 baths to every 3 bedrooms https://www.propertyreporter.co.uk/at-home/what-is-the-ideal-bedroom-bathroom-ratio.html
            bedrooms = int(round(bathrooms * 1.6)) 

            #assume bedrooms account for 29% https://nahbclassic.org/fileUpload_details.aspx?contentTypeID=3&contentID=216616&subContentID=541360
            sq_footage = round((224*bedrooms*100)/29)

            #$185 price/sqft https://www.rocketmortgage.com/learn/price-per-square-foot#:~:text=The%20current%20median%20price%20per,or%20lower%20than%20this%20number.
            price = sq_footage * 185

            #randomly allocate property
            seller_id = randint(1,cities)

            #cap number of agents per sale at 3
            guess = randint(1,4)
            sample_house_agents = sample(agents, guess)

            print('HOUSE', house_address, bathrooms, bedrooms, sq_footage, price, city_id, office_id, seller_id, sample_house_agents)
            db.session.add(House(address=house_address, bathrooms=bathrooms, bedrooms=bedrooms, sq_footage=sq_footage, price=price, 
                                city_id=city_id, office_id=office_id, seller_id=seller_id, agents_houses=sample_house_agents))

            office_id += 1
        print('\n')
    db.session.commit()


if __name__ == "__main__":
    db.create_all()
    create_agents(50)
    create_sellers(50) #number of sellers must equal number of cities
    create_cities_and_buildings(cities=50)