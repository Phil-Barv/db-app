### Question: To test your solution you will need to create fictitious data 
### and ensure that the correct results are calculated from your SQL code.

#To achieve this, I tested all my sql results against python-generated results,
#as such this file should be run after create.py that populates the db

from dbapp import db, queries
from dbapp.models import agent, house, office, sale
from datetime import datetime

#search parameters for current month
currentMonth = datetime.utcnow().strftime('%Y-%m') + '-01'
nextMonth = datetime.utcnow().strftime('%Y-') + f"{(int(datetime.utcnow().strftime('%m'))+1):02d}" + '-01'

import unittest

class appClientTests(unittest.TestCase):

    ###Test correct query when getting top 5 agents
    def test_top_5_agents(self):

        #fetch sql query result
        result = [[j[0] for j in i] for i in queries.get_top_5_agents()]
        result = ' '.join(result[1])

        temp = ['Add Agent', 0]

        for agents in db.session.query(agent.Agent).all():

            revenue = []
            for commission in agents.commission_list:
                if (commission.date_added).strftime('%Y-%m-%d') >= currentMonth and (commission.date_added).strftime('%Y-%m-%d') < nextMonth:
                    revenue.append(commission.house_price)
            
            if sum(revenue) > temp[1]:
                temp = [f'Agent Full Name: {agents.firstname} {agents.lastname} - Company Email: {agents.email}', sum(revenue)]

        #print(temp, '\n\n', result[1])

        #the top agent should be in the list of top five agents
        self.assertIn(temp[0], result)


    def test_top_5_offices(self):
        
        #fetch sql query result
        result = [[j[0] for j in i] for i in queries.get_top_5_offices()]
        result = ' '.join(result[1])

        temp = ['Add Sales', 0]

        for offices in db.session.query(office.Office).all():

            revenue = []
            for sale in offices.sale_list:
                if (sale.date_added).strftime('%Y-%m-%d') >= currentMonth and (sale.date_added).strftime('%Y-%m-%d') < nextMonth:
                    revenue.append(sale.house_price)

            if sum(revenue) > temp[1]:
                temp = [f'{offices.address}', sum(revenue)]

        #print(temp[0], '\n\n', result[1][0][0])

        #the top office should in the list of top five agents
        self.assertIn(temp[0], result)


    def test_avg_selling_price(self):

        #fetch sql query result
        result = queries.get_avg_selling_price()[1][0][1]

        revenue, sale_count = 0, 0

        for sales in db.session.query(sale.Sale).all():

            if (sales.date_added).strftime('%Y-%m-%d') >= currentMonth and (sales.date_added).strftime('%Y-%m-%d') < nextMonth:
                revenue += sales.house_price
                sale_count += 1
                
        temp = f"${int(revenue/sale_count):,}" #use int to avoid failure due to rounding errors

        #print(temp, '\n\n', result[1])
        self.assertIn(temp, result)


    def test_avg_listing_time(self):

        #fetch sql query result
        result = queries.get_avg_listing_time()[1][0][1]

        days_lst = []

        for sales in db.session.query(sale.Sale).all():

            if (sales.date_added).strftime('%Y-%m-%d') >= currentMonth and (sales.date_added).strftime('%Y-%m-%d') < nextMonth:

                listing_date = ((db.session.query(house.House).get(sales.house_id)).date_added)
                days_lst.append(abs((sales.date_added - listing_date).days))
                
        temp = f"AVG {(sum(days_lst)/len(days_lst)):.2f} DAYS"

        #due to rounding errors, the two should almost be equal
        self.assertIn(temp, result)


if __name__ == '__main__':
    #the tests occassionally run into floating point errors (7/10 runs with unique data)... still haven't pinpointed the exact cause
    unittest.main()
    
