''' 
Basic code to get flask up and running, performs templating for pages
'''

from flask import Flask, render_template, request
import pyodbc
from pyodbc import connect 

import printq

#setting up database context
cnxn_info = printq.get_server_config()
cnxn = pyodbc.connect(cnxn_info) 
cursor = cnxn.cursor() #used for queries 

app = Flask(__name__) 

'''
Landing page. Currently just asks the users to supply their floor, 
and tells them what's the closest floor with a printer on it by querying
the db. 
DB: Table Printer{ Id int, floornum int, room int, toner double, typeofink int}
'''
@app.route('/', methods=['GET', 'POST'])
def root():
    floor = None

    if request.method == 'POST':
        floor = request.form['floornum'] 
        row = printq.closest_floor(cursor, floor, 3) 
        floor = row[0].Floornum
        print row 
    return render_template('login.html', result = floor)

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    if request.method == 'POST': 
        # grabs information from the forms
        username = request.form['username']
        password = request.form['password']

        # cursor used to send queries
        cursor = conn.cursor()
        # executes query
        query = 'SELECT * FROM member WHERE username=? \
                and password=HASHBYTES(\'SHA_256\', ?)' 
        cursor.execute(query, username, password)
        # stores the results in a variable
        data = cursor.fetchone()
        # use fetchall() if you are expecting more than 1 data row
        cursor.close()
        error = None
        if (data):
            # creates a session for the the user
            # session is a built in
            session['username'] = username
            return redirect(url_for('home'))
        else:
            # returns an error message to the html page
            error = 'Invalid login or username'
            return render_template('login.html', error=error)
    return render_template('login.html', error=None) 

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/report')
def register():
    return render_template('report.html')
  
app.secret_key = 'bina'
app.run('localhost', 13000, debug=True)
