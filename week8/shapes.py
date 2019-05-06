
shapes = {
    3: "Triangle",
    4: "Quadrilateral",
    5: "Pentagon",
    6: "Hexagon",
    7: "Heptagon",
    8: "Octagon",
}

def getShape(sides):
    if sides in shapes.keys():
        return shapes[sides]
    else:
        return "?"

def printAllShapes():
    for i in range(3,9):
        print("A(n) %s has %d sides." % (getShape(i), i))



if __name__ == '__main__':
    printAllShapes()
