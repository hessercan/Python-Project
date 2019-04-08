def main():
  car = {}
  car["make"] = input("Make:  ")
  car["model"] = input("Model:  ")
  car["color"] = input("Color:  ")
  car["year"] = input("Year:  ")

  print("You have a %s %s %s %s" %
    (car["color"], car["year"], car["make"], car["model"]))

main()
exit()
