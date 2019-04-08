# Adds some space
print()

def checkYear(year):
# LeapYear Logic
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                leapyear = True
            else:
                leapyear = False
        else:
            leapyear = True
    else:
        leapyear = False

    return leapyear

quitWord = "quit"
year = ""

while year != quitWord:
    year = input("Year: ")

    if year == quitWord:
        print("Quit Word has been entered.")
    elif checkYear(int(year)):
        print(str(year) + " is a Leap Year")
    else:
        print(str(year) + " is NOT a Leap Year")

    # Adds some space
    print()

print("We've reached the end my friend. Good Bye")
quit()
