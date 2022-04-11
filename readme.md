# DB-APP_162

This is a Database app that realistically models a large realtor company with multiple property listings, agents, locations, and sellers. The app is built on the Flask micro-framework, using SQLAlchemy database models to capture the relationships between the data and flask-login that restricts data access to admins. 

The dashboard features long-term summaries while the collapsable sidebar offers views of each data model. Detailed analytics of the data are available by clicking on the Analystics button, and monthly summaries via the Monthly Insights button. As of now, the views have been implemented for view-only purposes rather than edit/update purposes. 

Make sure to populate the database using the automated system specifically created to emulate real-world data with its high scalability, distinct individuals, houses, offices, cities and generation of sales between 2021 and 2023 for the full experience.


### Getting the app running

1. Clone the repo to your local machine!
2. Open your terminal and cd to the location of the cloned repo.
3. In the clone's root directory, input:

#### macOS
```python3
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3.6 create.py #required to populate database
python3.6 app.py
```

#### Windows
```python3
python3.6 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3.6 create.py
python3.6 app.py
```

#### Git Bash
```python3
python3.6 -m venv venv
venv/Scripts/activate.bat
pip3 install -r requirements.txt
python3.6 create.py
python3.6 app.py
```

4. Once you run the commands, the app will spool up and give you a link in the terminal (usually: http://127.0.0.1:5000/). If you choose to automatically populate the database, it will take some time to generate and add data but once it does you will be provided with admin login details
that you can use to access the platform.

5. Paste the URL link into your favorite browser (Google Chrome is recommended) and voila! You now have a database management system. Enjoy!

As a side note, the app also features 4 in-built tests to confirm that the required SQL queries return the right results. You can run them once you have populated the database by using the following command:

```python3
python3.6 test.py
```
