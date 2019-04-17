def main():
    mainMenu()
    return 0

def mainMenu():
    strings = "hello"
    int1 = 1

    menuChoices = {
        1 : {'desc': "Print String", 'func': printstring, 'args': (strings)},
        2 : {'desc': "Print String Int", 'func': printstringint, 'args': (strings, int)},
        "Q" : {'desc': "Exit/Quit", 'func': quit, 'args': ()},
    }
    print(menuChoices)
    menu('Main Menu', 'Enter Choice: ', menuChoices, loop=True)

def printstringint(string, int):
    print(string,int)

def printstring(string):
    print(string)

def menu(heading, prompt, choices, loop=False):
    while True:
        print("\n" + heading)
        for key,choice in choices.items():
            print("%6s: %s" % (key, choice['desc']))
        i = input(prompt).upper()

        if i.isdigit():
            i = int(i)

        if i in choices.keys():
            if 'func' in choices[i] and choices[i]['func']:
                choices[i]['func'](*choices[i]['args'])
            if not loop:
                break
        else:
            print("Bad Choice")

main()
