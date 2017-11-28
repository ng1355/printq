''' 
Basic code to get flask up and running, performs templating for pages
'''

from flask import Flask, render_template, request

app = Flask(__name__) 

@app.route('/', methods=['GET', 'POST'])
def root():
    floor = None
    if request.method == 'POST':
        floor = request.form['floor'] 
    return render_template('login.html', result = floor)

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM member WHERE username = %s and password = MD5(%s)'
    cursor.execute(query, (username, password))
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

@app.route('/register')
def register():
    return render_template('register.html')

app.secret_key = 'bina'
app.run('localhost', 13000, debug=True)
