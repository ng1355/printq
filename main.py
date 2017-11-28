''' 
Basic code to get flask up and running, performs templating for pages
'''

from flask import Flask, render_template, request, session, redirect, url_for
import pyodbc
from pyodbc import connect 
from flask_googlemaps import GoogleMaps, Map

import printq

#setting up database context
cnxn_info = printq.get_server_config()
cnxn = pyodbc.connect(cnxn_info) 
cursor = cnxn.cursor() #used for queries 


app = Flask(__name__) 

#setting up gmaps
app.config['GOOGLEMAPS_KEY'] = printq.get_api_key()
GoogleMaps(app) 

'''
Landing page. Currently just asks the users to supply their floor, 
and tells them what's the closest floor with a printer on it by querying
the db. 
'''
@app.route('/', methods=['GET', 'POST'])
def root():
    if 'username' not in session:
        return redirect(url_for('login'))

    floor = None
    gmap = printq.gen_map()
    if request.method == 'POST':
        try: 
            floor = request.form['floornum'] 
            int(floor)
        except ValueError:
            return render_template('root.html', result = None)
        row = printq.closest_floor(cursor, floor, 3) 
        floor = row[0].Room
    return render_template('root.html', result = floor, gmap=gmap)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('root')) 

    if request.method == 'POST': 
        # grabs information from the forms
        username = request.form['username']
        password = request.form['password']

        # executes query
        query = 'SELECT * FROM users WHERE username=? \
                and password=HASHBYTES(\'SHA1\',?)' 
        cursor.execute(query, username, password)
        # stores the results in a variable
        data = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        error = None
        if (data):
            # creates a session for the the user
            # session is a built in
            session['username'] = username
            return redirect(url_for('root'))
        else:
            # returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('login.html', error=error)
    return render_template('login.html', error=None) 

@app.route('/register', methods=['GET', 'POST']) 
def register(error=None):
    if 'username' in session:
        return redirect(url_for('root')) 

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = 'select * from users  where username = ?'
        cursor.execute(query, username) 
        data = cursor.fetchone() 
        if(data is None):
            query = 'insert into users(username, password) \
                    values (?,HASHBYTES(\'SHA1\',?))' 
            cursor.execute(query, username, password) 
            cursor.commit()
            session['username'] = username
            return redirect(url_for('root'))
        else:
            error = 'Username taken' 
            return render_template('register.html', error=error) 
    return render_template('register.html')

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/settings')
def register():
    return render_template('settings.html')

@app.route('/seeall')
def register():
    return render_template('seeall.html')

@app.route('/logout', methods=['GET']) 
def logout():
    if 'username' in session:
        session.pop('username', None) 
    return redirect(url_for('root')) 

app.secret_key = 'bina' #do NOT share this
app.run('localhost', 13000, debug=True)
