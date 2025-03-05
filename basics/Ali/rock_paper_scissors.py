import random

options = ("rock", "paper", "scissors")
running = True

while running:

    player = None
    computer = random.choice(options)

    while player not in options:
        player = input("Enter your move: (rock, paper, scissors): ")

    print(f"Player played {player}")
    print(f"Computer played {computer}")

    if player == computer:
        print("It's a tie!")
    elif player == "rock" and computer == "scissors":
        print("You got a point!")
    elif player == "paper" and computer == "rock":
        print("You got a point!")
    elif player == "scissors" and computer == "paper":
        print("You got a point!")
    else:
        print("computer got a point!")

    if not input("Play again? (y/n): ") == "y":
        running = False

print("Thanks for playing!")
    
    

    

