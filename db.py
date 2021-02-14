import psycopg2
from config import Config

params = Config()

# connect to the PostgreSQL server
print("Connecting to the PostgreSQL database...")
conn = psycopg2.connect(
    database=params.DATABASE, 
    user = params.USER, 
    password = params.PASSWORD, 
    host = params.HOST, 
    port = params.PORT)

# create a cursor
cur = conn.cursor()

# execute a statement
print("PostgreSQL database version:")
cur.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cur.fetchone()
print(db_version)

# close the communication with the PostgreSQL
cur.close()