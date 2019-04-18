import os

# Main Database Initialization
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



# Clears the Terminal to help keep things clean.
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print(appHeader)

# Main Menu Selection
# Returns the users choice.
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

# Prints the Main Menu to the User.
def printMenu():
    print("P:  Print all inventory")
    print("A:  Add a new part")
    print("L:  Lookup part by number")
    print("R:  List parts that are low on inventory")
    print("Q:  Exit/Quit")

# Prints the Add Remove Inventory Menu.
def printARMenu():
    print("A: Add Inventory")
    print("R: Remove Inventory")
    print("Q: Go Back")

# Prints All Inventory in Alphanumeric order.
def printInventory():
    global database
    clear()
    print(inventoryHeader)

    # Sorts the Dictionary in Alphanumeric order.
    for key in sorted(database.keys()):
        print(partInfo(key))
    wait()

# Adds New Part to the Database
# *Prompts the User for Part Infomation
# *Verifies that the Part doesn't already Exists
# *Verifies that the user is entering numbers only when required.
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
    # Prints new part to the user.
    print(inventoryHeader)
    print(partInfo(key))
    wait()

# Lookup by Part Number
# Prompts the User to Enter the Part Number
# Requries a Number to be entered
def lookupPart():
    global database
    clear()

    # Add Remove Inventory Menu
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

# Add Remove Inventory Menu
# Returns the Users Choice if Valid
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

# Requires a part number (key)
# Adds inventory to the part provided
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

# Requires a part number (key)
# Removes inventory to the part provided
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

# Does Absolutly Nothing...
# Required to exit Add Remove Menu
def quitInventory(part):
    return "q"

# Prints All Parts with Inventory Lower than four (4)
def lowInventory():
    clear()
    print("Parts that are Low on Inventory:")
    print(inventoryHeader)
    for key in sorted(database.keys()):
        if database[key][1] < 4:
            print(partInfo(key))
    wait()

# Requires Part Number (key)
# Builds String from the key provided
def partInfo(part):
    string = part
    string = string + "\t\t" + str(database[part][1])
    string = string + "\t\t" + str(database[part][0])
    return string

# Allows program to wait for user input before continuing
def wait():
    input("Press Enter to Continue: ")

# Overrides Quit Method
# Clears the Terminal and Prints a Farewell message before Exiting
def quit():
    clear()
    print("Thanks for Playing! Goodbye...")
    exit()

# Main Menu Dictionary
menu = {
    "p": printInventory,
    "a": addPart,
    "l": lookupPart,
    "r": lowInventory,
    "q": quit
}

# Program Loop
# Runs until Quit Method is run
while True:
    menu[mainmenu()]()
