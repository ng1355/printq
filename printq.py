from flask_googlemaps import Map

def get_server_config(config_file = '../printq_config'):
   config = open(config_file, 'r') 
   DRIVER = config.readline().strip()
   SERVER =  config.readline().strip()
   DATABASE =  config.readline().strip()
   UID =  config.readline().strip()
   PWD =  config.readline().strip()
   cnxn = 'DRIVER=%s;SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % \
           (DRIVER, SERVER, DATABASE, UID, PWD) 
   config.close()
   return cnxn

def get_api_key(api_path = '../apikey'):
    f = open(api_path, 'r') 
    key = f.read().strip()
    f.close()
    return key

def closest_floor(cursor, floornum, limit = 1):
    cursor.execute('select * from printer \
            where room != \'library\' order by ABS(floornum - ?)', floornum)
    return cursor.fetchmany(limit)  

def closest_loc(cursor, lat, lng, limit = 1):
    cursor.execute('select * from printer \
            order by ABS(latitude - ?) and ABS(longitude - ?)', lat, lng) 
    return cursor.fetchmany(limit) 

def gen_map(print_markers = None):
    return Map(
        lat=40.6942036,
        lng=-73.986579,
        zoom=13,
        style = 'height: 400px; \
                width: 100%;', 
        markers = print_markers,
        varname = 'gmaps',
        identifier = 'gmap',
        )
