''' 
Basic code to get flask up and running, performs templating for pages
'''

from flask import Flask, render_template, request
import pyodbc

server = '' 

app = Flask(__name__) 

@app.route('/', methods=['GET', 'POST'])
def root():
    floor = None
    if request.method == 'POST':
        floor = request.form['floor'] 
    return render_template('root.html', result = floor)

app.secret_key = 'bina'
app.run('localhost', 13000, debug=True)
