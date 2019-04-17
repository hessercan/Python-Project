# SouthHills
# Created by Chris Coble
#
# Inventory management script.
#

import sys

inventory = {
    1 : {'desc': 'Wireless Mouse', 'stock': 3, 'archived': False},
    2 : {'desc': 'Wireless Keyboard', 'stock': 3, 'archived': False},
    3 : {'desc': '19" Monitor', 'stock': 2, 'archived': False},
    4 : {'desc': '23" Monitor', 'stock': 2, 'archived': False},
    5 : {'desc': 'HDMI Cable', 'stock': 5, 'archived': False},
    6 : {'desc': 'VGA Cable', 'stock': 5, 'archived': False},
    7 : {'desc': 'USB Cable', 'stock': 10, 'archived': False},
    8 : {'desc': 'Power Cable', 'stock': 5, 'archived': False},
    9 : {'desc': '8GB Thumb Drive', 'stock': 3, 'archived': False},
    10 : {'desc': '16GB Thumb Drive', 'stock': 4, 'archived': False}
}

def main():
    mainMenu()
    return 0

# prompt user with main menu until quit
def mainMenu():
    menuChoices = {
        'P' : {'desc': 'Print all inventory', 'func': printInventory, 'args': ()},
        'A' : {'desc': 'Add a new part', 'func': newPart, 'args': ()},
        'L' : {'desc': 'Lookup part by number', 'func': lookupPart, 'args': ()},
        'R' : {'desc': 'List parts that are low on inventory', 'func': lowInventory, 'args': ()},
        'X' : {'desc': 'Archive a part', 'func': archivePart, 'args': ()},
        'Q' : {'desc': 'Exit/Quit', 'func': quit, 'args': ()}
    }
    menu('Main Menu', 'Enter Choice:  ', menuChoices, loop=True)

def quit():
    sys.exit(0)

# print entire inventory, do not print archived parts
def printInventory(parts=None):
    parts = inventory if parts == None else parts
    print("Part Number      # In Stock         Part Description")
    for partNum,partInfo in parts.items():
        if not partInfo['archived']:
            print("%04d             %-4d               %s" % (partNum, partInfo['stock'], partInfo['desc']))

# add a new part type to the inventory
def newPart():
    newPartNum = int(len(inventory) + 1)
    partInfo = {}
    partInfo['desc'] = input("Enter part description:  ")
    partInfo['stock'] = getIntFromUser("Enter number in stock:  ")
    partInfo['archived'] = False
    inventory[newPartNum] = partInfo

# Display info about a part by part number and
# allow user to add/remove pieces to inventory.
# For archived parts, just print part number & description
def lookupPart():
    partnum = getPartNumFromUser("Enter part number:  ", len(inventory))

    if inventory[partnum]['archived']:
        printPart(partnum, inventory[partnum]['desc'], None)
        print("Part is archived!")
        return
    else:
        printPart(partnum, inventory[partnum]['desc'], inventory[partnum]['stock'])

    partMenu = {
        'A' : {'desc': 'Add Inventory of this part', 'func': addInventory, 'args': (partnum,)},
        'R' : {'desc': 'Remove inventory of this part', 'func': removeInventory, 'args': (partnum,)},
        'M' : {'desc': 'Return to main menu', 'func': None}
    }
    menu('What do you want to do?', 'Enter Choice:  ', partMenu, loop=False)

# set part's archived flag
def archivePart():
    partnum = getPartNumFromUser("Enter part number:  ", len(inventory))
    inventory[partnum]['archived'] = True

# add more pieces to a specified part
def addInventory(partnum):
    inventory[partnum]['stock'] += getIntFromUser('How many? ')

# remove pieces of a specified part
def removeInventory(partnum):
    while True:
        userNumber = getIntFromUser('How many? ')
        if userNumber <= inventory[partnum]['stock']:
            inventory[partnum]['stock'] -= userNumber
            return
        else:
            print('There are only %d parts in inventory!' % inventory[partnum]['stock'])

# print info of a specified part
# instock can be set to None to indicate archived part
def printPart(partnum, desc, instock):
    print("")
    print("Part Number:  %04d" % partnum)
    print("Description:  %s" % desc)
    if instock is not None:
        print("# In Stock:  %d" % instock)
    print("")

# print parts that are low on inventory
def lowInventory():
    # create dictionary of just the parts that are low then print that
    lowInStock = { }
    for partNum,partInfo in inventory.items():
        if partInfo['stock'] < 3:
            lowInStock[partNum] = partInfo
    print("The following parts are low on inventory")
    printInventory(lowInStock)

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

# display menu and get user slection
# heading is a string that is printed before menu options
# prmopt is a string that is printed when asking user for input
# choices is a dictionary for the menu.  Key is a string, it is the menu option.
# the value of the dictionary is another dictionary that has these key/values
#       1.  'desc' : Menu choice description
#       2.  'func' : Function to call if this choice is selected
#       3.  'args' : Argument list to pass to 'func'
def menu(heading, prompt, choices, loop):
    while True:
        # Print the menu and get user choice
        print("\n" + heading)
        for key,choice in choices.items():
            print("%6s:  %s" % (key, choice['desc']))
        userChoice = input(prompt).upper()

        # check if choice is valid
        if userChoice in choices.keys():
            # check if there is a function to be called for this choice
            if 'func' in choices[userChoice] and choices[userChoice]['func']:
                choices[userChoice]['func'](*choices[userChoice]['args'])
            if not loop:
                break
        else:
            badChoice()

def badChoice():
    print('Invalid choice')

sys.exit(main())
