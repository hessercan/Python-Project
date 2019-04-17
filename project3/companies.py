# Mark Hesser
# HesserCAN
# mark@hessercan.com
# Project 3
# Company Stock Information

import os
import json
import operator

# Constant Strings
APPHEADER = "Company Stock Information \nHesserCAN"
PROMPT = "Enter Choice: "

# Clears Terminal and Initiates Main Menu.
def main():
    clear()
    mainMenu()
    return 0

# Display Main Menu to the user.
def mainMenu():
    menuChoices = {
        1 : {'desc': "Find company by stock symbol", 'func': findByStockSymbol, 'args': ()},
        2 : {'desc': "Find company by name", 'func': findByName, 'args': ()},
        3 : {'desc': "Find company by sector", 'func': findBySector, 'args': ()},
        4 : {'desc': "Display Top Ten Viewed", 'func': displayTopTen, 'args': ()},
        "Q" : {'desc': "Exit/Quit", 'func': quit, 'args': ()},
    }
    menu('Main Menu', 'Enter Choice: ', menuChoices, loop=True)

# Prompts the user to enter a Stock Symbol.
# Creates a Menu of Companies to choose from.
def findByStockSymbol():
    clear()
    print("\nFind Company By Stock Symbol")
    symbol = input("Search: ")

    printCompanyInfo(symbol.upper())

# Prompts the user to enter a keyword to search company by name.
# Creates a Menu of Companies to choose from.
def findByName():
    clear()
    print("\nFind Company By Name")
    name = input("Search: ")

    namesMenu = {}
    counter = 1
    for symbol,company in database.items():
        if company['companyName']:
            if name.lower() in company['companyName'].lower():
                desc = str("(%s) %s" % (symbol,company['companyName']))
                namesMenu[counter] = {'desc': desc, 'func': printCompanyInfo, 'args': ([symbol])}
                counter += 1

    namesMenu['M'] = {'desc': "Return to the Main Menu", 'func': clear, 'args': ()}

    menu("Available Companies (Search: %s): " % (name), PROMPT, namesMenu, loop=False)

# Lists all available sectors to user to choose from
def findBySector():
    clear()
    sectorMenu = {}

    counter = 1
    for symbol,company in sectors.items():
        desc = "%s (%d)" % (symbol, len(company))
        #print(desc) # Debug Code
        sectorMenu[counter] = {'desc': desc, 'func': findCompanyBySector, 'args': ([symbol])}
        counter += 1

    sectorMenu['M'] = {'desc': "Return to the Main Menu", 'func': clear, 'args': ()}

    menu("Find Company by Sector. \nAvailable Sectors: ", PROMPT, sectorMenu, loop=False)

# List all companys from provided sector.
def findCompanyBySector(sector):
    companiesMenu = {}

    symbols = sectors.get(sector, 'none')

    counter = 1
    for symbol in symbols:
        desc = str(database[symbol].get('companyName', 'none'))
        companiesMenu[counter] = {'desc': desc, 'func': printCompanyInfo, 'args': ([symbol])}
        counter += 1

    companiesMenu['M'] = {'desc': "Return to the Main Menu", 'func': clear, 'args': ()}

    menu("Find Company by Sector. \nAvailable Companies: ", PROMPT, companiesMenu, loop=False)

# Prints Company Information by symbol.
def printCompanyInfo(symbol):
    global database

    clear()
    print()

    companyInfo = database.get(symbol, "none")
    if companyInfo and companyInfo != 'none':
        print("Company Name: %s" % (companyInfo['companyName']))
        print("Stock Symbol: %s" % (symbol))
        print("Description: %s" % (companyInfo['description']))
        print("CEO: %s" % (companyInfo['CEO']))
        print("Website: %s" % (companyInfo['website']))
        database[symbol]['viewed'] += 1
    else:
        print("Company not found.")

# Displays a Menu of the Top 10 Viewed Companies
def displayTopTen():
    clear()

    # Gathering viewed companies by symbol
    viewed = {}
    for symbol,company in database.items():
        if company['viewed'] > 0:
            viewed[symbol] = company['viewed']
    #print(viewed)

    viewedMenu = {}
    if len(viewed.values()) > 0:
        s_viewed = sorted(viewed.items(), key=operator.itemgetter(1), reverse=True)
        counter = 1
        for s in s_viewed:
            if counter <= 10:
                desc = str("%s (Viewed: %d)" % (s[0],s[1]))
                viewedMenu[counter] = {'desc': desc, 'func': printCompanyInfo, 'args': ([s[0]])}
                counter += 1

        viewedMenu['M'] = {'desc': "Return to the Main Menu", 'func': clear, 'args': ()}

        menu("Top Ten Viewed Companies: ", PROMPT, viewedMenu, loop=False)
    else:
        print("No Companies have been Viewed.")

# It is guaranteed that this function will return a positive number
# Do not return until user enters a valid number
def getIntFromUser(prompt):
    while True:
        string = input(prompt)
        if string.isdigit():
            return int(string)
        else:
            print("Not a valid number")

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

# Print "Invalid Choice" to the terminal.
def badChoice():
    clear()
    print('Invalid choice. Please Try Again.')

# Clears the Terminal to help keep things clean.
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    print(APPHEADER)

# Allows program to wait for user input before continuing.
def wait():
    input("Press Enter to Continue: ")

# Clears the Terminal and Prints a Farewell message before Exiting
# Overrides Quit Method
def quit():
    clear()
    print("Thanks for Playing! Goodbye...")
    exit()

# Prompts the user for the file location.
# Returns filename as a string.
def getFileLocation():
    filename = input("Load which json file: ")
    if filename:
        return str(filename)
    else:
        return 'companies.json'

# Loads json data into a dictionary,
# sorts the information into easier to manage dictionaries.
def loadData():
    global sectors
    global database

    with open(getFileLocation()) as f:
        jsondata = json.load(f)

    # key: Symbol
    # value: dictionary with company information
    for c in jsondata:
        database[str(c['symbol'])] = {
            'companyName': c['companyName'],
            'exchange': c['exchange'],
            'industry': c['industry'],
            'website': c['website'],
            'description': c['description'],
            'CEO': c['CEO'],
            'issueType': c['issueType'],
            'sector': c['sector'],
            'viewed': 0
        }

    for company in jsondata:
        if 'sector' in company.keys():
            sector = company['sector']
            symbol = company['symbol']

            if sector and sector != 'None':
                if not sector in sectors:
                    sectors[sector] = []
                sectors[sector].append(symbol)

# Databases in the form of Dictionaries.
sectors = {}
database = {}

loadData()
main()
