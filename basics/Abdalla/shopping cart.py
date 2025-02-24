items = ("apple","banna","orange","milk","bread")
shoping_cart = []
print("menu: apple,orange,banna,milk,bread")
print("options")
print("1.add an item")
print("2. remove an item")
print("3.view items in cart")
print("4.check if an item is in stock")
print("5.exit")
choice = input("enter your choice: ")
while True:
    if choice == "1":
        item = input("enter item to add:  ")
        if item in items:
            shoping_cart.append
        else:
            print(f"sorry we dont have{item}")
    if choice == "2":
        item = input("enter item to remove:  ")
        if shoping_cart in item:
            shoping_cart.remove
        else:
            print("that item isnt in the shoping cart")
    if choice == "3":
        print(f"the items in your cart are:{shoping_cart}")
    if choice == "4":
        item = input("enter an item to check if it is in stock")
    if item in items:
        print(f"{item} is in stock")
    else:
        print("sorry we dont have this item")
    if choice == "5":
        break
    else:
        print("invaild choice try again")         
