import leaguepedia_parser
import psycopg2
from time import sleep
from collect import *
from create_tables import create_tables


# psycopg2.OperationalError: FATAL:  the database system is starting up
conn = psycopg2.connect(
    host="db",
    database="pro_league",
    user="admin",
    password="admin")

def connect(conn):
    """ Connect to the PostgreSQL database server """
    try:
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    # connect(conn)
    create_tables(conn)
