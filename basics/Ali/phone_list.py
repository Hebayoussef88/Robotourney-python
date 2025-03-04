#----------phone list----------
print("----------phone list----------")
phone_list = {"ali":18183838, "ahmed":8383883383, "zyad": 49835734957}
print (phone_list)
add = str(input("add? "))
if add == "True":
    ask = int(input("how many people to add"))
    for i in range(ask):
        x = input("person ")
        y = input("number ")
        phone_list[x] = y
        print(phone_list)
else:
    print("ok")
remove = str(input("remove? "))
if remove == "True":
    ask1 = int(input("how many people to remove"))
    for i in range(ask1):
        x = input("person ")
        phone_list.pop(x)
        print(phone_list)
else:
    print("ok")
check = str(input("check? "))
if check == "True":
    ask2 = int(input("how many people to check"))
    for i in range(ask2):
        x = input("person ")
        phone_list.get(x)
        if x in phone_list:
            print("found")
        else:
            print("not found")
else:
    print("ok")

Print("--------------------done--------------------")
