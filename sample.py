# sample comment in code

# If Else Statements
condition1 = False
condition2 = True

if condition1 and condition2:
    print("Both Conditions are True")
elif condition1:
    print("The 1st Condition is True")
elif condition2:
    print("The 2nd Condition is True")
else:
    print("Both Conditions are False!")

# Add some spacing
print()

# While Loops
i = 1
j = 3

while i <= j:
    # If the index is even
    if i % 2 == 0:
        print(str(i) + " is Even")
    else:
        print(str(i) + " is Odd")
    i+=1

# Add some spacing
print()

# For Loops
start = 4
end = 11

for i in range(start, end):
    # If the index is even
    if i % 4 == 0:
        print(str(i) + " is a Quad Bro")
    else:
        print(str(i) + " is not with the Quads")

# Add some spacing
print()

# Quit the program
print("We've reached the end my friend. Good Bye")
quit()
