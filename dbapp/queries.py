from dbapp import db
from sqlalchemy.sql import text
from datetime import datetime

#Indices on dates have been immplemented for faster queries as I use dates to filter results in the where clauses
#This practice is inline with this article: https://stackoverflow.com/questions/107132/what-columns-generally-make-good-indexes

currentMonth = datetime.utcnow().strftime('%Y-%m') + '-01'
nextMonth = datetime.utcnow().strftime('%Y-') + f"{(int(datetime.utcnow().strftime('%m'))+1):02d}" + '-01'

def get_top_5_agents(db=db):

    qry = text(
                "SELECT agent.firstname, agent.lastname, agent.email, SUM(commission.house_price) as revenue, COUNT(*) "
                "FROM agent "
                "INNER JOIN commission ON commission.agent_id = agent.id "
               f"WHERE DATE(commission.date_added) BETWEEN '{currentMonth}' AND '{nextMonth}' "  #end date is exclusive
                "GROUP BY agent.firstname "
                "ORDER BY revenue DESC LIMIT 5 "
        )

    result = db.session.execute(qry)

    #create list to render in frontend
    info_list = ['Top Five Agents | Most Revenue', 
                [[ f"Agent Full Name: {i[0]} {i[1]} - Company Email: {i[2]}", "${:,.2f}".format(i[3]), i[4]] for i in result]]

    return info_list

def get_top_5_offices(db=db):

    #technically industry standard is to check net profit rather than number of sales but both have been captured here
    qry = text(
                "SELECT office.address, SUM(sale.house_price) AS revenue, COUNT(*) AS sales "
                "FROM office "
                "INNER JOIN sale ON sale.office_id = office.id "
               f"WHERE DATE(sale.date_added) BETWEEN '{currentMonth}' AND '{nextMonth}' "  #end date is exclusive
                "GROUP BY office.address "
                "ORDER BY revenue DESC LIMIT 5 "
        )

    result = db.session.execute(qry)

    #create list to render in frontend
    info_list = ['Top Five Offices | Most Revenue', [[ i[0], "${:,.2f}".format(i[1]), i[2]] for i in result]]
    return info_list

def get_avg_selling_price(db=db):

    #For all houses that were sold that month, calculate the average selling price

    qry = text(
               "SELECT house.address, AVG(sale.house_price), COUNT(*)"
               "FROM house "
               "INNER JOIN sale ON sale.house_id = house.id "
              f"WHERE DATE(sale.date_added) BETWEEN '{currentMonth}' AND '{nextMonth}' "  #end date is exclusive
        )

    result = db.session.execute(qry)

    #create list to render in frontend
    info_list = ['Average Selling Price | Monthly Data',[[ f"Houses sold: 1. {i[0]}, . . .","${:,.2f} AVG".format(i[1]), i[2]] for i in result]]
    
    return info_list


def get_avg_listing_time(db=db):

    #For all houses that were sold that month, calculate the average number of days that the houses were on the market.
    #datediff as described in this article did not work https://www.sqlservertutorial.net/sql-server-date-functions/sql-server-datediff-function/

    qry = text(
            "SELECT house.address, house.date_added, sale.date_added "
            "FROM house "
            "INNER JOIN sale ON sale.house_id = house.id "
            f"WHERE DATE(sale.date_added) BETWEEN '{currentMonth}' AND '{nextMonth}' "  #end date is exclusive
             "GROUP BY house.address "
    )

    result = db.session.execute(qry)

    from datetime import datetime

    #process date deltas
    data = [[i[0], datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S.%f'), datetime.strptime(i[2], '%Y-%m-%d %H:%M:%S.%f')] for i in result]
    days = [abs((i[2] - i[1]).days) for i in data]

    info_list = ['Average Listing Time | Monthly Data', [[ f"Houses sold: 1. {data[0][0]}, . . .","AVG {:,.2f} DAYS".format(sum(days)/len(days)), len(days)]]]
   
    return info_list