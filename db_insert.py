import sqlite3
from sqlite3 import Error
from datetime import datetime
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#temp = '34.23'
#humi = '65.34'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO dht(extract_date,temperature,humidity)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def main():
    database = "database.db"
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    date = datetime.today().strftime('%Y-%m-%d')
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        dht = (date, temp, humi);
        project_id = create_project(conn, dht)

if __name__ == '__main__':
    main()