import random
computer_choise = random.randint(0,100)
print("Please Choose Number between 0 >> 100 ")
while True:
    user_choise= int(input("Enter Your Guess: "))
    if user_choise >= 0 and user_choise <= 100:
        if user_choise < computer_choise:
            print("the number is Higher than it ")
        if user_choise > computer_choise:
            print("the number is lorwer than it ")
        if user_choise == computer_choise:
            print("You Guessed Correctly ")
            break
    else:
        print("not valid input")

