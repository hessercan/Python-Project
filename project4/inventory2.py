import os
import sqlite3
from sqlite3 import Error

# Final Strings
APPHEADER = "Inventory Management"
INVENTORYHEADER = "Part Number:  ~ In-Stock:    ~  Description:"
PROMPT = "Enter choice from menu above: "
DBFILE = "inventory2.db"

# Global database connection used to process SQLite queries.
dbconn = None

# Creates a connection to the inventory2 database
# Checks to see if the parts table exists and if not initializes it
# Enters the main program
# Closes the database connection when finished.
def create_connection(db_file):
    global dbconn
    # create a database connection to a SQLite database
    try:
        dbconn = sqlite3.connect(db_file)
        if not checkTableExists(dbconn, "parts"):
            initdatabase(dbconn)
        main()
    except Error as e:
        print(e)
    finally:
        dbconn.close()

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{0}';
        """.format(tablename.replace('\'', '\'\'')))
    result = dbcur.fetchone()
    print(result)
    if result[0] == 1:
        dbcur.close()
        return True
    else:
        dbcur.close()
        return False

def initdatabase(conn):
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS parts(ID INTEGER PRIMARY KEY AUTOINCREMENT,description Varchar,inventory INTEGER, archived INTEGER DEFAULT 0);")

    initdbdata = [
        ('Wireless Mouse', 3),
        ('Wireless Keyboard', 3),
        ('19\" Monitor', 2),
        ('23\" Monitor', 2),
        ('HDMI Cable', 5),
        ('VGA Cable', 5),
        ('USB Cable', 10),
        ('Power Cable', 5),
        ('8GB Thumb Drive', 3),
        ('16GB Thumb Drive', 4),
    ]
    try:
        sql = "INSERT INTO parts ('description','inventory') VALUES(?,?);"
        c.executemany(sql, initdbdata)
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0]) # column name is not unique
    c.close()
    conn.commit()

# Clears Terminal and Initiates Main Menu.
def main():
    clear()
    mainMenu()
    return 0

# Display Main Menu to the user.
def mainMenu():
    menuChoices = {
        "P" : {'desc': "Print Active Inventory", 'func': printInventory, 'args': ()},
        'PA' : {'desc': 'Print All Inventory', 'func': printInventory, 'args': ([2])},
        'PX' : {'desc': 'Print Archived Inventory', 'func': printInventory, 'args': ([1])},
        "A" : {'desc': "Add a new part", 'func': addPart, 'args': ()},
        "L" : {'desc': "Lookup part by number", 'func': lookupPart, 'args': ()},
        "R" : {'desc': "List parts that are low on inventory", 'func': lowInventory, 'args': ()},
        'X' : {'desc': 'Archive a part', 'func': archivePart, 'args': ()},
        "Q" : {'desc': "Exit/Quit", 'func': quit, 'args': ()},
    }
    menu('Main Menu', PROMPT, menuChoices, loop=True)

# Prints All Inventory in Alphanumeric order.
# archive 0: prints all inventory
# archive 1: prints all active inventory
# archive 2: prints all archived inventory
def printInventory(archive=0):
    clear()
    print(INVENTORYHEADER)

    c = dbconn.cursor()

    sql = "SELECT * FROM parts;"
    c.execute(sql)

    result = c.fetchall()
    for r in result:
        if archive == 0:
            if r[3] == 0:
                print(partInfo(r))
        elif archive == 1:
            if r[3] == 1:
                print(partInfo(r))
        elif archive == 2:
            print(partInfo(r))
    if archive > 0:
        print("* = Archived")

    c.close()


# Adds New Part to the Database
# *Prompts the User for Part Infomation
# *Verifies that the Part doesn't already Exists
# *Verifies that the user is entering numbers only when required.
def addPart():
    global dbconn
    clear()
    print("Add a new part.")

    # Verfiy's Data Entered is Valid
    isValid = False
    desc = input("Please Enter the Description: ")
    while not isValid:
        inv =  input("Please Enter Initial Inventory: ")
        if inv.isdigit():
            isValid = True
        else:
            print("Invalid Entry, Please enter a number.")

    c = dbconn.cursor()

    sql = '''INSERT INTO parts ('description','inventory') VALUES(?,?);'''
    c.execute(sql,(desc,inv))

    sql = "SELECT * FROM parts WHERE description='%s'" % (desc)
    part = c.execute(sql).fetchone()
    # Prints new part to the user.
    print(INVENTORYHEADER)
    print(partInfo(part))
    c.close()
    dbconn.commit()

# Lookup by Part Number
# Prompts the User to Enter the Part Number
# Requries a Number to be entered
def lookupPart():
    clear()
    partnum = getPartNumFromUser("Enter part number:  ", getMax())

    c = dbconn.cursor()
    sql = "SELECT * FROM 'parts' WHERE ID=%s;" % (partnum)
    result = c.execute(sql).fetchone()
    c.close()

    print(INVENTORYHEADER)
    print(partInfo(result))
    if result[3] == 1:
        print("Part has been archived")
    else:
        partMenu = {
            "A" : {'desc': "Add Inventory", 'func': addInventory, 'args': ([result])},
            "R" : {'desc': "Remove Inventory", 'func': removeInventory, 'args': ([result])},
            'M' : {'desc': "Return to the Main Menu", 'func': clear, 'args': ()}
        }
        menu("What would you like to do?", PROMPT, partMenu)

def addInventory(part):
    global dbconn
    c = dbconn.cursor()
    change = getIntFromUser("Add How Many: ")
    total = part[2] + change
    sql = "UPDATE 'parts' SET inventory=%d WHERE ID=%d;" % (total,part[0])
    c.execute(sql)
    c.close()
    dbconn.commit()

def removeInventory(part):
    c = dbconn.cursor()
    change = getIntFromUser("Remove How Many: ")
    total = part[2] - change
    sql = "UPDATE 'parts' SET inventory=%d WHERE ID=%d;" % (total,part[0])
    c.execute(sql)
    c.close()
    dbconn.commit()

# Prints All Parts with Inventory Lower than four (4)
def lowInventory():
    clear()
    print("Parts that are Low on Inventory:")
    print(INVENTORYHEADER)

    c = dbconn.cursor()
    sql = "SELECT * FROM 'parts';"
    c.execute(sql)
    result = c.fetchall()
    for r in result:
        if r[2] < 5:
            if r[3] == 0:
                print(partInfo(r))

    c.close()


def archivePart():
    global dbconn
    clear()
    partnum = getPartNumFromUser("Enter part number:  ", getMax())

    c = dbconn.cursor()
    sql = "SELECT * FROM 'parts' WHERE ID=%s;" % (partnum)
    result = c.execute(sql).fetchone()
    if result[3] == 0:
        sql = "UPDATE 'parts' SET 'archived'=1 WHERE ID=%d;" % (result[0])
    else:
        sql = "UPDATE 'parts' SET 'archived'=0 WHERE ID=%d;" % (result[0])
    c.execute(sql)

    sql = "SELECT * FROM 'parts' WHERE ID=%d" % (result[0])
    result = c.execute(sql).fetchone()
    c.close()
    dbconn.commit()

    print(INVENTORYHEADER)
    print(partInfo(result))

def partInfo(part):
    s = ""
    if part[3] == 1:
        s = s + "* "
    s = s + "%.4d" % (part[0])
    s = s + "\t\t"
    s = s + str(part[2])
    s = s + "\t\t"
    s = s + str(part[1])

    return s

# Displays a menu and get a selection from the user.
# heading: a string that is printed before the menu options.
# prompt: a string that is printed when asking the user for input.
# choices: a Dictionary for the menu. The key is a string, it is the menu option.
# the value of the dictionary is another dictionary that has these key/values
#   'desc': Menu choice description
#   'func': Function to call if this choice is selected
#   'args': Argument list to pass to 'func'
# loop: tells the infinite loop to break if false. default is false.
def menu(heading, prompt, choices, loop=False):
    while True:
        print("\n" + heading)
        for key,choice in choices.items():
            print("%6s: %s" % (key, choice['desc']))
        userChoice = input(prompt).upper()

        if userChoice.isdigit():
            userChoice = int(userChoice)

        if userChoice in choices.keys():
            if 'func' in choices[userChoice] and choices[userChoice]['func']:
                #print(str(choices[userChoice]['func'](*choices[userChoice]['args'])))
                choices[userChoice]['func'](*choices[userChoice]['args'])
            if not loop:
                break
        else:
            badChoice()

def getMax():
    c = dbconn.cursor()
    sql = "SELECT COUNT('ID') FROM 'parts';"
    max = c.execute(sql).fetchone()[0]
    c.close()
    return max

# It is guaranteed that this function will return a part
# number that exists in inventory
# Do not return until user enters an existing part number.
def getPartNumFromUser(prompt, max):
    while True:
        partnum = getIntFromUser(prompt)
        if partnum > 0 and partnum <= max:
            return partnum
        else:
            print("Part does not exist!")

# It is guaranteed that this function will return a positive number
# Do not return until user enters a valid number
def getIntFromUser(prompt):
    while True:
        string = input(prompt)
        if string.isdigit():
            return int(string)
        else:
            print("Not a valid number")

# Print "Invalid Choice" to the terminal.
def badChoice():
    clear()
    print('Invalid choice. Please Try Again.')

# Clears the Terminal to help keep things clean.
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print(APPHEADER)

# Clears the Terminal and Prints a Farewell message before Exiting
# Overrides Quit Method
def quit():
    clear()
    print("Thanks for Playing! Goodbye...")
    dbconn.close()
    exit()

# Allows program to wait for user input before continuing.
def wait():
    input("Press Enter to Continue: ")

create_connection(DBFILE)
