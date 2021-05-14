"""
Use this code to insert data from DHT22 to SQLite Database

"""
import sqlite3
from sqlite3 import Error
from datetime import datetime
# Library for DHT22
import Adafruit_DHT

# Initialize Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
# Sensor GPIO
DHT_PIN = 4


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
    database = "/home/pi/dht_sensor/database.db"
    humi, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    date = datetime.today().strftime('%Y-%m-%d %H:%M')
    # create a database connection
    conn = create_connection(database)
    with conn:
        # read dht
        temp = round(temp,3)
        humi = round(humi,3)
        dht = (date, temp, humi);
        project_id = create_project(conn, dht)
        print(dht)

if __name__ == '__main__':
    main()
