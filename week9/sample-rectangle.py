
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def getArea(self):
        return (self.width * self.height)

    def getPerimeter(self):
        return ((2 * self.width) + (2 * self.height))

# Prints All Attributes of a Rectangle Object
def printRectangle(rectangle):
    print("Width = {}".format(rectangle.width))
    print("Height = {}".format(rectangle.height))
    print("Perimeter = {}".format(rectangle.getPerimeter()))
    print("Area = {}".format(rectangle.getArea()))

rect = Rectangle(10,5)
rect2 = Rectangle(6,8)

printRectangle(rect)
printRectangle(rect2)
