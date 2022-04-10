from dbapp import db
from dbapp.models import buyer, seller
from sqlalchemy import text

def get_top_seller():
    #tried this advanced query using sqlalchemy but would not load relational data, returned only Trues and Falses
    #https://stackoverflow.com/questions/65480238/why-am-i-unable-to-generate-a-query-using-relationships

    temp = ['Add Clients', 0]

    for client in db.session.query(seller.Seller).all():
        if len(client.houses) > temp[1]:
            temp = [f'Seller {client.id}: {client.firstname} {client.lastname}', len(client.houses)]

    return temp


def get_top_buyer():

    temp = ['Add Clients', 0]

    for client in db.session.query(buyer.Buyer).all():
        if len(client.sales) > temp[1]:
            temp = [f'Buyer {client.id}: {client.firstname} {client.lastname}', len(client.sales)]

    return temp


def get_top_agent():

    temp = [['Add Agents', 0]]

    qry = text(
                "SELECT agent.id, agent.firstname, agent.lastname, SUM(commission.house_price) AS revenue, COUNT(*) AS sales "
                "FROM agent "
                "INNER JOIN commission ON commission.agent_id = agent.id "
                "GROUP BY agent.firstname "
                "ORDER BY sales DESC LIMIT 1 "
        )

    result = db.session.execute(qry)

    #create list to render in frontend
    temp = [[ f"Agent {i[0]}: {i[1]} {i[2]}",  i[4]] for i in result]

    return temp[0]


def get_top_office():

    temp = [['Add Sales', 0]]

    qry = text(
            "SELECT office.id, office.address, SUM(sale.house_price) AS revenue, COUNT(*) AS sales "
            "FROM office "
            "INNER JOIN sale ON sale.office_id = office.id "
            "GROUP BY office.address "
            "ORDER BY revenue DESC LIMIT 1 "
    )

    result = db.session.execute(qry)

    #create list to render in frontend
    temp = [[ f"Office {i[0]}: {i[1][:13]} . . .",  i[3]] for i in result]

    return temp[0]


def get_all_listings():

    temp = [['Add Sales', 0]]

    qry = text(
            "SELECT house.id, house.address, COUNT(*)"
            "FROM house "
            "WHERE house.is_sold = 0"
    )

    result = db.session.execute(qry)

    #create list to render in frontend
    temp = [[ f"Houses Listed: [House {i[0]}: {i[1]}. . .]",  i[2]] for i in result]

    return temp[0]


###python alternative
# def get_top_agent():

#     temp = ['Add Agents', 0]

#     for agents in db.session.query(agent.Agent).all():
#         if len(agents.sales) > temp[1]:
#             temp = [f'Agent {agents.id}: {agents.firstname} {agents.lastname}', len(agents.sales)]

#     return temp