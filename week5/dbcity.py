import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        initdb(conn)
        printRecords(conn)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

def initdb(conn):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS us")
    c.execute("CREATE TABLE IF NOT EXISTS us(ID INTEGER PRIMARY KEY AUTOINCREMENT,city Varchar,state Varchar,population Int);")

    initdbdata = [
      ('New York City', 'New York', 8550000),
      ('Los Angeles', 'California', 3970000),
      ('Chicago', 'Illinois', 2720000),
      ('Houston', 'Texas', 2300000),
      ('Philadelphia', 'Pennsylvania', 1570000),
    ]

    try:
        sql = '''INSERT INTO us ('city','state','population') VALUES(?,?,?);'''
        c.executemany(sql, initdbdata)
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0]) # column name is not unique
    conn.commit()

def printRecords(conn):
    c = conn.cursor()
    c.execute("SELECT city,state,population FROM us ORDER BY population DESC")
    for record in c:
        city,state,population = record
        print("%s, %s: %.2f million" % (city,state,population/1000000))

if __name__ == '__main__':
    create_connection('citypop.db')
