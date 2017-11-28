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
        '''
        cursor.execute('select top 1 * from floors \
        where printer = 1 order by ABS(floor - ?)', floor)
        row = cursor.fetchone() 
        floor = row.floor
        '''
        row = printq.closest_floor(cursor, floor, 3) 
        floor = row[0].Floornum
        print row 
    return render_template('root.html', result = floor)

app.run('localhost', 13000, debug=True)
