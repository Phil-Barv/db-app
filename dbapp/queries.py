from flask import session
from dbapp import db
from dbapp.models import agent, buyer, city, house, office, sale, seller
from sqlalchemy import desc, func

def get_top_seller():
    #tried this advanced query using sqlalchemy but would not load relational data, returned only Trues and Falses
    #https://stackoverflow.com/questions/65480238/why-am-i-unable-to-generate-a-query-using-relationships

    temp = ['Add Clients', 0]

    for client in db.session.query(seller.Seller).all():
        if len(client.houses) > temp[1]:
            temp = [f'{client.firstname} {client.lastname}', len(client.houses)]

    return temp


def get_top_sellers():
    qry = (db.session.query(seller.Seller)
                .select_from(house.House)
                .join(house.House.sellers_houses)
                .with_entities(seller.Seller.houses))

    print(qry[0])


def get_top_buyer():

    temp = ['Add Clients', 0]

    for client in db.session.query(buyer.Buyer).all():
        if len(client.sales) > temp[1]:
            temp = [f'{client.firstname} {client.lastname}', len(client.sales)]

    return temp

def get_top_agent():

    temp = ['Add Agents', 0]

    for agents in db.session.query(agent.Agent).all():
        if len(agents.sales) > temp[1]:
            temp = [f'{agents.firstname} {agents.lastname}', len(agents.sales)]

    return temp


from collections import Counter


def get_top_office():

    temp = ['Add Sales', 0]
    offices = []

    for hse in db.session.query(house.House).all():
        if hse.is_sold:
            offices.append(hse.office)

    if len(offices) > 0:
        frequency = Counter(offices)

        top_offices = [str(name).split(',')[0] for name, count in frequency.items() if count == max(frequency.values())]
        top_offices = ', '.join(map(str, top_offices))

        return top_offices, max(frequency.values())

    return temp


def test_query():

    qry = (db.session
                  .query(agent.Agent.lastname, office.Office.address, func.sum(sale.Sale.house_price))
                  .join(agent.Agent, sale.Sale.agents_sales == agent.Agent.sales)
                  .join(office.Office, agent.Agent.offices == office.Office.agents_offices)
                  .group_by(agent.Agent.id)
                  .orderby(desc(func.sum(sale.Sale.house_price)))
                  .limit(5)
    )

    print(qry)
        