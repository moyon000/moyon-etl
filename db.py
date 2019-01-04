# pyodbc para conectarse por ODBC
import pyodbc
# diccionario de dbs contiene dsn,db,uid,pwd
import config

# INICIA CONEXION CON LA BD
def connect_start(self):
	try:
		conn = pyodbc.connect('DSN=%s;database=%s;UID=%s;PWD=%s'
        	%(self.dsn,self.db,self.uid,self.pwd))
		print('conexion %s OK' %(self.name))
		return conn.cursor()
	except Exception as error:
		print('conexion %s FAIL, Error: %s' %(self.name,type(error)))
		
# OBJETO BD 
# se le pasa el name de la db
class database(object):
	"""docstring for database"""	
	def __init__(self, name):
		super(database, self).__init__()
		# Reporte el config en 5 variables => NAME,DSN,DATABASE,USERNAME,PASSWORD 
		self.name,self.dsn,self.db,self.uid,self.pwd = config.dbs[name].values()
		self.cursor = connect_start(self)	# INICIO CONEXION
