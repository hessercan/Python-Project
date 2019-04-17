import json

with open("ancestry.json") as f:
    data = json.load(f)

def main():
    getChildren(0, data)

def getChildren(gen, parent):
    prefix = "\t" * gen
    for person in parent:
        print("%s%s, born in %s" % (prefix, person['name'], person['born']))
        if 'children' in person:
            getChildren(gen + 1, person['children'])

main()
