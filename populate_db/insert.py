from dbapp import db
from dbapp.models import administrator, agent, buyer, city, commission, house, office, sale, seller

from random import choices, sample, randint, choice
from populate_db.libraries import all_cities_with_zipcodes


import datetime
#generate random sales between these dates --> make sure range includes the current month you're in
start_date = datetime.date(year=2020, month=11, day=1)
end_date = datetime.date(year=2023, month=4, day=4)

from datetime import datetime
from faker import Faker

fake = Faker()

def create_admin():

    admin_exists = administrator.Admins.query.filter_by(email='admin@dundermifflin.com').first()

    if admin_exists == None:
        new_admin = administrator.Admins(name='admin', email='admin@dundermifflin.com', password='admin')

        try:
            db.session.add(new_admin)
            db.session.commit()
            print("Database population complete.\n\nLogin using credentials\nemail: admin@dundermifflin.comn\npassword: admin")

        except:
            pass #no need to do anything if admin alread exists


def create_agents(agents):

    print('\nGenerating Agents Data. This might take a while...\n')

    for _ in range(agents):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = f"{firstname.lower()}.{lastname.lower()}@dundermifflin.com"
        
        #generic password for all test agents
        password = "Fizz"

        #check if agent already exists before adding them -> maintain unique users for testing
        agent_exists = agent.Agent.query.filter_by(email=email).first()

        if agent_exists == None:
            db.session.add(agent.Agent(firstname=firstname, lastname=lastname, email=email, password=password))
    
    #commit as a single transaction
    db.session.commit()
    print('\nCompleted Generating Agents Data\n')


def create_sellers(sellers):

    print('\nGenerating Sellers Data...\n')
    
    for _ in range(sellers):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = f"{firstname.lower()}.{lastname.lower()}{choice(['@gmail.com', '@hotmail.com', '@yahoo.com', '@outlook.com'])}"
        
        #generic password for all test sellers
        password = "Buzz"

        #check if seller already exists before adding them -> names may overlap with agents but emails are unique
        seller_exists = seller.Seller.query.filter_by(email=email).first()

        if seller_exists == None:
            db.session.add(seller.Seller(firstname=firstname, lastname=lastname, email=email, password=password))
    
    #commit as a single transaction
    db.session.commit()
    print('\nCompleted Generating Sellers Data.\n')

def create_buyers(sellers):

    print('\nGenerating Buyers Data...\n')
    
    for _ in range(sellers):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = f"{firstname.lower()}.{lastname.lower()}{choice(['@gmail.com', '@hotmail.com', '@yahoo.com', '@outlook.com'])}"
        
        #generic password for all test sellers
        password = "FizzBuzz"

        #check if buyer already exists before adding them -> names may overlap with agents but emails are unique
        buyer_exists = buyer.Buyer.query.filter_by(email=email).first()

        if buyer_exists == None:
            db.session.add(buyer.Buyer(firstname=firstname, lastname=lastname, email=email, password=password))
    
    #commit as a single transaction
    db.session.commit()
    print('\nCompleted Generating Buyers Data.\n')


def create_cities_and_buildings(cities):

    #get all agents and sellers from db
    agents = agent.Agent.query.all()
    sellers = seller.Seller.query.all()

    #carry out samples on cities
    sample_cities = sample(list(all_cities_with_zipcodes.values()), cities) #remove duplicates if any

    print('\nGenerating City, Office and House Data.\n')

    for city_id in range(len(sample_cities)):

        #create city
        city_created = False

        try:
            db.session.add(city.City(name=sample_cities[city_id][0], zip_code=sample_cities[city_id][1], state=sample_cities[city_id][2]))
            city_created = True

        except:
            city_created = False
            pass


        if city_created:

            guess0 = randint(10, len(sample_cities)) 

            #generate identifying data
            city_address = f'{sample_cities[city_id][0]}'

            for id in range(guess0):

                guess = randint(1, 20)

                #round to .5 as you can have .5 baths in real estate
                bathrooms = guess/2  #low-.5, high-10
                
                #assume ratio of 1.8 baths to every 3 bedrooms https://www.propertyreporter.co.uk/at-home/what-is-the-ideal-bedroom-bathroom-ratio.html
                bedrooms = round(bathrooms * 1.6)

                #assume bedrooms account for 29% ~ 3.448276 https://nahbclassic.org/fileUpload_details.aspx?contentTypeID=3&contentID=216616&subContentID=541360
                sq_footage = round(((224-(40/guess))* bathrooms * 1.6 *3.448276), 2)

                #listing fee (to spread values out)
                listing_fee = 1+ (guess/100)

                #$185 price/sqft https://www.rocketmortgage.com/learn/price-per-square-foot#:~:text=The%20current%20median%20price%20per,or%20lower%20than%20this%20number.
                price = round((sq_footage * (185-(40/guess)) * listing_fee), 2)


                #cap number of agents per sale at 4, owners at 2
                guess1, guess2, guess3 = randint(1,9), randint(1,4), randint(1,2)

                #randomly allocate property to singles or couples
                seller_id = choices(sellers, k=guess3)

                #sample randomly
                sample_office_agents = sample(agents, guess1)
                sample_house_agents = sample(agents, guess2)

                #give each house a fictitious address
                zip_code = randint(10000,99999)
                house_address = f'{fake.street_name()}, {zip_code} {city_address}'
                office_address = f'{fake.street_name()}, {zip_code} {city_address}'

                try:
                    db.session.add(office.Office(address = office_address, city_id = city_id+1, agents_offices=sample_office_agents))
                    db.session.add(house.House(address=house_address, bathrooms=bathrooms, bedrooms=bedrooms, sq_footage=sq_footage, price=price, 
                                    city_id=city_id+1, office_id=id+1, sellers_houses=seller_id, agents_houses=sample_house_agents))

                except:
                    pass

    #print('\n')
    db.session.commit()
    print('\nCompleted Generating City, Office and House Data.\n')


def calculate_commission(price, agents):
    # For houses sold below $100,000 the commission is 10%
    # For houses between $100,000 and $200,000 the commission is 7.5%
    # For houses between $200,000 and $500,000 the commission is 6%
    # For houses between $500,000 and $1,000,000 the commission is 5%
    # For houses above $1,000,000 the commission is 4%
    # split evenly among number of agents involved in sale

    commissions = {
        'tier_5': 0.1,
        'tier_4': 0.075,
        'tier_3': 0.06,
        'tier_2': 0.05,
        'tier_1': 0.04
    }
    
    price  = float(price)

    if price >= 1000000:
        comm_percent = commissions['tier_1'] * 100
        total_comm = round((commissions['tier_1'] * price), 2)
        comm = round(total_comm/agents, 2)

        return total_comm, comm, comm_percent

    elif price >= 500000:        
        comm_percent = commissions['tier_2'] * 100
        total_comm = round((commissions['tier_2'] * price), 2)
        comm = round(total_comm/agents, 2)
        
        return total_comm, comm, comm_percent

    elif price >= 200000:
        comm_percent = commissions['tier_3'] * 100
        total_comm = round((commissions['tier_3'] * price), 2)
        comm = round(total_comm/agents, 2)
        
        return total_comm, comm, comm_percent

    elif price >= 100000:
        comm_percent = commissions['tier_4'] * 100
        total_comm = round((commissions['tier_4'] * price), 2)
        comm = round(total_comm/agents, 2)
        
        return total_comm, comm, comm_percent

    else:
        comm_percent = commissions['tier_5'] * 100
        total_comm = round((commissions['tier_5'] * price), 2)
        comm = round(total_comm/agents, 2)
        
        return total_comm, comm, comm_percent


def create_sales_and_commissions():

    all_houses = house.House.query.all()
    all_buyers = buyer.Buyer.query.all()

    guess = len(all_buyers) #least sales are 10

    sample_buyers = sample(all_buyers, guess)
    sample_houses = sample(all_houses, guess)

    print('\nGenerating Sales and Commissions Data.\n')

    for buyers in range(len(sample_buyers)):

        agents = [agent.Agent.query.get(a.id) for a in sample_houses[buyers].agents_houses]
        house_price = sample_houses[buyers].price
        house_id = sample_houses[buyers].id
        house_office_id = house.House.query.get(house_id).office_id
        comm = calculate_commission(house_price, len(agents))

        sale_date = fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
        sale_time = f" {randint(1,11):02d}:{randint(0,59):02d}:{randint(0,59):02d}"
        date_obj = datetime.strptime(sale_date+sale_time, '%Y-%m-%d %H:%M:%S')

        try:
            comm_list = []

            for agent_id in agents:
                #print(f'Commission: Sale ID {buyers+1} Agent ID {agent_id.id} House Price {house_price} Commission {comm[1]} Percentage {comm[2]}%')
                
                new_commission = commission.Commission(sale_id=buyers+1, agent_id=agent_id.id, house_price=house_price,
                                                     comm_amount=comm[1], comm_percent=comm[2], date_added=date_obj)

                db.session.add(new_commission)

                comm_list.append(new_commission) #comm object not comm amount

            new_owners = sample(all_buyers, randint(1, 2)) #simulate single or couple owned

            #print(f'Sale: House ID: {house_id} Sold: {True} Commissions {comm_list} Agents {agents} Buyers {new_owners} \n')

            (db.session.add(sale.Sale(house_id=house_id, office_id=house_office_id, date_added=date_obj, commission_list=comm_list, 
                                      agents_sales=agents, house_price=house_price, buyers_sales=new_owners)))
                                      
            house_to_update = house.House.query.get(house_id)
            house_to_update.is_sold = True

        except:
            pass #do nothing if fails

    #print('\n')
    db.session.commit()
    print('\nCompleted Generating Sales and Commissions Data.\n')