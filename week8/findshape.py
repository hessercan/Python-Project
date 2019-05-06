import shapes

def main():
    while True:
        try:
            s = int(input("Enter number of Side: "))
            break
        except Exception as e:
            raise


    print("A(n) %s has %d sides." % (shapes.getShape(s), s))

main()
