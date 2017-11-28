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
