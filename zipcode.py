d = {
    "10001":"New York City",
    "10002":"New York City",
    "90001":"Los Angeles",
    "90002":"Los Angeles",
    "90003":"Los Angeles",
    "73301":"Austin",
    "75001":"Dallas",
    "60007":"Chicago",
    "33101":"Miami",
    "20001":"Washington D.C."
}

def searchZips(city):
    found = []
    for k,v in d.items():
        if v.lower() == city.lower():
            found.append(k)

    print("Zipcodes for " + city + ":")

    if not found:
        print("None Found")
    else:
        for f in found:
            print(f)

userSearch = input("Enter a City Name: ")
searchZips(userSearch)
