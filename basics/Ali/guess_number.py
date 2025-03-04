# guess the number
print("guess the number")
print("----------------")
import random
numbers = random.randint(0, 100)
print("guess from 0 to 100")
while True:
    answer = int(input("enter the number"))
    if answer > numbers:
        print("a bit lower")
    if answer < numbers:
        print("a bit higher")
    if answer == numbers:
        print("correct")
        quit()
else:
    print("invalid")

