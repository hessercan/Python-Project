# Mark Hesser
# HesserCAN
# www.hessercan.com
# Python Mid-Term Exam

import json
import sqlite3
from sqlite3 import Error
import sys

print("HesserCAN Mid-Term Exam!")

# Problem 1
def countByTwo(number):
    print()
    if str(number).isdigit():
        count = 2
        while count <= number:
            print(count)
            count += 2

# Problem 2
names = []
def fillNames():
    print()
    global names
    for i in range(0,3):
        isValid = False
        while not isValid:
            name = input("Please Enter a Name: ")
            if name.lower() in names:
                print("That name already Exists, Please Try Again.")
            else:
                names.append(name.lower())
                isValid = True

# Problem 3
def printDogs():
    print()
    with open('dogs.json') as f:
        jsondata = json.load(f)

    #print(jsondata)
    for item in jsondata:
        print("%s is a %s." % (item['name'], item['breed']))
        if 'humans' in item.keys():
            members = len(item['humans'])
            print("%s has %d human family members." % (item['name'], members))
        else:
            print("%s needs a home." % item['name'])

# Problem 4
def addVehicle(vin, make, model, year):
    print()
    # create a database connection to a SQLite database
    try:
        dbconn = sqlite3.connect('vehicles.db')
        c = dbconn.cursor()
        c.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
        result = c.fetchall()
        if len(result)==0:
            sql = '''INSERT INTO vehicles ('vin','make','model','year') VALUES(?,?,?,?);'''
            c.execute(sql,(vin,make,model,year))
        else:
            print("Vehicle Already in the Database.")

        dbconn.commit()

    except Error as e:
        print(e)
    finally:
        sql = "SELECT * FROM vehicles"
        c.execute(sql)
        result = c.fetchall()
        print("Vehicle List: ")
        for r in result:
            print("   %.4d %s %s" % (r[3], r[1], r[2]))
        c.close()
        dbconn.close()



countByTwo(10)
fillNames()
printDogs()
addVehicle('D534FR', 'Ford', 'Escape', 2013)
sys.exit(0)
