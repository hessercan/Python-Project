# sample json import
# in-class assignment

import json

with open("schedule.json") as f:
    data = json.load(f)
    #print(data)
    print("Your Schedule:")
    for item in data:
        print("%s %s, %s at %s (%s): %s"
        % (item['month'], item['day'], item['year'], item['time'],
        item['location'], item['description']) )
