
class Shape:
    def __init__(self,color):
        self.color = color
        self.width = "n/a"
        self.height = "n/a"

    def getName(self):
        return "Generic Shape"

    def getColor(self):
        return self.color

    def getArea(self):
        raise Exception("Can't get Area")

    def getPerimeter(self):
        raise Exception("Can't get Perimeter")

# Retangle Inherits Shape
class Rectangle(Shape):
    def __init__(self, color, width, height):
        self.width = width
        self.height = height
        self.color = color

    # Override
    def getName(self):
        return "Rectangle"

    def getArea(self):
        return (self.width * self.height)

    def getPerimeter(self):
        return ((2 * self.width) + (2 * self.height))

# Prints All Attributes of a Shape Object
def printShape(s,n):
    try:
        print("Shape {} is a {} {}".format(n,s.color, s.getName()))
        print("\tSize: {} x {}".format(s.width, s.height))
        print("\tPerimeter: {}".format(s.getPerimeter()))
        print("\tArea: {}".format(s.getArea()))
    except Exception as e:
        print("\tError")

shape1 = Shape("Red")
shape2 = Rectangle("Blue",5,10)

printShape(shape1,1)
printShape(shape2,2)
