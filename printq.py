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

def closest_floor(cursor, floornum, limit = 1):
    cursor.execute('select * from printer \
            order by ABS(floornum - ?)', floornum)
    return cursor.fetchmany(limit)  

def closest_room(cursor, room, limit = 1):
    
    room = room.rstrip('AB') 
    cursor.execute('select top 1 * from printer \
            order by ABS(room - ?)', room) 
