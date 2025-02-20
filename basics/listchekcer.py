print("list checker")
list = ["ali", "zyad", "abdallah", "khadija"]
name = str(input("your name?"))
if name in list:
    print(f"{name} is found on the list")
else:
    print(f"{name} is not found on the list")
    print("too bad so sad!!")
