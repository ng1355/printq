''' 
Basic code to get flask up and running, performs templating for pages
'''

from flask import Flask, render_template, request
import pyodbc
from pyodbc import *

#setting up database context
server = 'tcp:0.0.0.0,1401' #ip for docker
database = 'printq'
username = 'SA'
password = 'two(2)Chunks' 
offline = False

'''
If the db cant be reached, go set offline flag and go on without it. 
with the offline flag on, all client side functionality will be dumb, 
but functional. I might remove this cause it makes the script really slow. 
'''
try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' \
            +server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor() #used for queries 
except:
    offline = True 

app = Flask(__name__) 

'''
Landing page. Currently just asks the users to supply their floor, 
and tells them what's the closest floor with a printer on it by querying
the db. 
'''
@app.route('/', methods=['GET', 'POST'])
def root():
    floor = None
    global offline #hopefully we can find a better way to keep this state

    if request.method == 'POST':
        floor = request.form['floor'] 
        if offline is False:
            try:
                #calculates closest floor with a printer 
                #TODO: gracefully handle malformed queries
                #eg: submitting "Choose one..." as an option 
                cursor.execute('select top 1 * from floors \
                 where printer = 1 order by ABS(floor - ?)', floor)
                row = cursor.fetchone() 
                floor = row.floor
            except:
                offline = True
    return render_template('root.html', result = floor)

app.run('localhost', 13000, debug=True)
