import os

database = {
    "0001": ["Wireless Mouse", 3],
    "0002": ["Wireless Keyboard", 3],
    "0003": ["19\" Monitor", 2],
    "0004": ["23\" Monitor", 2],
    "0005": ["HDMI Cable", 5],
    "0006": ["VGA Cable", 5],
    "0007": ["USB Cable", 10],
    "0008": ["Power Cable", 5],
    "0009": ["8GB Thumb Drive", 3],
    "0010": ["16GB Thumb Drive", 4],
}

appHeader = "Inventory Management"
inventoryHeader = "Part Number:  ~ In-Stock:    ~  Description:"

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print(appHeader)

def mainmenu():
    clear()
    isValid = False
    while not isValid:
        printMenu()
        choice = input("Enter choice from menu above: ").lower()

        if choice in menu:
            isValid = True
        else:
            clear()
            print("That is not a Valid Choice!")

    return choice

def printMenu():
    print("P:  Print all inventory")
    print("A:  Add a new part")
    print("L:  Lookup part by number")
    print("R:  List parts that are low on inventory")
    print("Q:  Exit/Quit")

def printARMenu():
    print("A: Add Inventory")
    print("R: Remove Inventory")
    print("Q: Go Back")

def printInventory():
    global database
    clear()
    print(inventoryHeader)

    for key in sorted(database.keys()):
        print(partInfo(key))
    wait()

def addPart():
    global database
    clear()
    print("Add a new part.")

    # Verfiy's Data Entered is Valid
    isValid = False
    while not isValid:
        key = input("Please Enter the Part Number: ")
        if key not in database.keys():
            if key.isdigit():
                desc = input("Please Enter the Description: ")
                while not isValid:
                    inv =  input("Please Enter Initial Inventory: ")
                    if inv.isdigit():
                        isValid = True
                    else:
                        print("Invalid Entry, Please enter a number.")
            else:
                print("Invalid Entry, Please enter a number.")
        else:
            print("Part Already Exists.")

    # Add new part to database
    database[key] = [str(desc),int(inv)]
    print(inventoryHeader)
    print(partInfo(key))
    wait()

def lookupPart():
    global database
    clear()
    menu = {
        "a": addInventory,
        "r": removeInventory,
        "q": quitInventory,
    }

    key = None
    while key != "q":
        #clear()
        print("Lookup part by number, Enter q to Quit")
        key = input("Please Enter the Part Number: ")
        part = database.get(key, "none")

        print(inventoryHeader)
        if part == "none":
            print("Unknown Part")
        else:
            print(partInfo(key))
            menu[inventoryMenu()](key)

def inventoryMenu():
    isValid = False
    while not isValid:
        printARMenu()
        choice = input("Enter choice from menu above: ").lower()

        if choice in menu:
            isValid = True
        else:
            clear()
            print("That is not a Valid Choice!")

    return choice

def addInventory(part):
    global database
    isValid = False
    while not isValid:
        number = input("Add How Many: ")
        if number.isdigit():
            isValid = True
        else:
            print("That is not a number...")
    database[part][1] += int(number)

def removeInventory(part):
    global database
    isValid = False
    while not isValid:
        number = input("Add How Many: ")
        if number.isdigit():
            isValid = True
        else:
            print("That is not a number...")
    database[part][1] -= int(number)

def quitInventory(part):
    return "q"

def lowInventory():
    clear()
    print("Parts that are Low on Inventory:")
    print(inventoryHeader)
    for key in sorted(database.keys()):
        if database[key][1] < 4:
            print(partInfo(key))
    wait()

def partInfo(part):
    string = part
    string = string + "\t\t" + str(database[part][1])
    string = string + "\t\t" + str(database[part][0])
    return string

def wait():
    input("Press Enter to Continue: ")

def quit():
    clear()
    print("Thanks for Playing! Goodbye...")
    exit()

menu = {
    "p": printInventory,
    "a": addPart,
    "l": lookupPart,
    "r": lowInventory,
    "q": quit
}

while True:
    menu[mainmenu()]()
