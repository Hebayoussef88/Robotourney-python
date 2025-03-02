import random

def guess_the_number():
    
    number_to_guess = random.randint(1, 100)
    attempts = 0
    guessed_correctly = False

    print("welcome to the Guess the number game")
    print("I am thinking of a number between 1 and 100")

    while not guessed_correctly:
            
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                guessed_correctly = True
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
        


guess_the_number()
