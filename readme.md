# DB-APP_162

This is a Database app that models a large realtor company with multiple property listings, agents, locations, and sellers. The app is built on the Flask micro-framework, using SQLAlchemy database models to store the data.


### Getting the app running

1. Clone the repo to your local machine!
2. Open your terminal and cd to the location of the cloned repo.
3. In the clone's root directory, input:

#### macOS
```python3
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3.6 populate.py #skip if database population not required
python3.6 app.py
```

#### Windows
```python3
python3.6 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3.6 populate.py #skip if database population not required
python3.6 app.py
```

#### Git Bash
```python3
python3.6 -m venv venv
venv/Scripts/activate.bat
pip3 install -r requirements.txt
python3.6 populate.py #skip if database population not required
python3.6 app.py
```

4. Once you run the commands, the app will spool up and give you a link in the terminal (usually: http://127.0.0.1:5000/). If you choose to automatically populate the database, it will take some time to generate and add data.
5. Paste the link into your favorite browser (Google Chrome is recommended) and voila! You now have a task management system. Enjoy!
