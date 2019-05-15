'''
Write a python script that continuously ask the user to enter car information.
For each car, the user will enter the make/model/year.
Your python code must create a new Car object each time the user enters a car.
Your code must maintain a a list of Car objects.
Each car will be represented by a class that you define, the class will be named Car.
When a Car object is created, the make, model, and year of the car must be specified when instantiating the object.
The Car class must have methods getMake(), getModel(), and getYear().
After each time the user enters another car, print all of the cars that the user has entered.
User can enter 'quit' to exit.
'''

class Car:
    # Init Constructor
    def __init__(self, make, model, year):
            self.make = make
            self.model = model
            self.year = year

    # Returns the make of the car
    def getMake(self):
        return self.make

    # Returns the model of the car
    def getModel(self):
        return self.model

    # Returns the year of the car
    def getYear(self):
        return self.year

cars = {}
count = 1

def main():
    while True:
        choice = input("Continue Entering Cars? (Y/N): ").upper()
        if choice == "N":
            break
        if choice != "Y":
            print("Try Again")
            continue

        createCar()
        printCars()


def createCar():
    print("Please enter the Make, Model and Year of the Car.")
    make = input("Make: ")
    model = input("Model: ")
    year = input("Year: ")

    global cars
    global count
    cars[count] = Car(make,model,year)
    count += 1


def printCars():
    print("\nAll Cars")
    for i,car in cars.items():
        print("Car %d: " % (i), end="")
        print("{} {} {}".format(car.getYear(), car.getMake(), car.getModel()))
    print()

main()
quit()
