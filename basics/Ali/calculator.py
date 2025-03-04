a = int(input("enter a number"))
b = int(input("enter a second number"))
ask1 = str(input("plus?"))
ask2 = str(input("minus?"))
ask3 = str(input("multiply?"))
ask4 = str(input("divide?"))
if ask1 == "yes":
    print(a + b)
elif ask1 == "no":
    print("ok")
if ask2 == "yes":
    print(a - b)
elif ask2 == "no":
    print("ok")
if ask3 == "yes":
    print(a * b)
elif ask3 == "no":
    print("ok")
if ask4 == "yes":
    print(a/b)
elif ask4 == "no":
    print("ok")