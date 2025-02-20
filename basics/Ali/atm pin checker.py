pin = 1083
for i in range(3):
    name = int(input("what is your pin?"))
    if name == pin:
        print("correct")
        exit()
    else:
        print("try again")
print("lockdown")
