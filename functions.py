# Sample Functions in Python

def main(j, k):
    for i in range(j,k):
        # Odd A
        if i % 2 != 0:
            functionA()
        # Even B
        else:
            functionB()

def functionA():
    print("Hi, this is Function Aaa")
def functionB():
    print("Hi, this is Function Bee")

main(1,21)

quit()
