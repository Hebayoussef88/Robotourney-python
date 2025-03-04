print("----------shopping cart----------")
item = []
length = int(input("enter your length "))
for i in range(length):
    items = input("enter an item ")
    item.append(items)
print(item)
print(len(item))
remove = bool(input("remove? "))
if remove == True:
    remove1_length = int(input("how many do you want to remove "))
    for i in range(remove1_length):
        remove2 = input("remove an item ")
        item.remove(remove2)
        print(len(item))
        print(item)
else:
    quit()
ask1 = bool(input("check for inputs? "))
if ask1 == True:
    ask1_length = int(input("how many do you want to check"))
    for i in range(ask1_length):
        ask2 = input("what do you want to check")
        if ask2 in item:
            print("found")
        else:
            print("not found")
else:
    print("ok")
    quit()





