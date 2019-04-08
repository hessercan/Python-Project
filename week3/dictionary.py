# in-class example

d = {
    "it101": "10:00",
    "ba200": "2:00",
    "cs100": "9:00" 
}

# This is a Lookup
time = d.get("it101", "(Unknown Time)")
print(time)

# This is a Search
found = []
for k,v in d.items():
    if v == "10:00":
        found.append(k)

for f in found:
    print(f)

quit()
