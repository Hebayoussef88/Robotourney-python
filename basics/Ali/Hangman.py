# hangman
print("Hangman")
print("*******")
import random
words = ["apple", "banana", "money", "computer", "desktop", "hangman"]
random_words = random.choice(words)
space = ["-"]*len(random_words)
print(space)
running = True
repeat1 = False
guessed_letters = []
trials = 6
states = ["""
             --------
              |     |
              |     O
              |    \\|/
              |     |
              |    / \\
             ---
             """,
             """
             --------
              |     |
              |     O
              |    \\|/
              |     |
              |    / 
             ---
             """,
             """
              --------
              |     |
              |     O
              |    \\|/
              |     |
              |     
             ---
             """,
             """
              --------
              |     |
              |     O
              |    \\|
              |     |
              |     
             ---
             """,
             """
              --------
              |     |
              |     O
              |     |
              |     |
              |     
             ---
             """,
             """
             --------
              |     |
              |     O
              |    
              |     
              |     
             ---
             """,
             """
              --------
              |     |
              |     
              |    
              |      
              |     
             ---
             """]
while running:
    ask = input("enter a letter ").lower()
    if len(ask) == 1 and ask.isalpha():
        if ask not in random_words:
            print("not found")
            trials -= 1
            guessed_letters.append(ask)
            print(guessed_letters)
        if ask in random_words:
            print("correct")
            for i in range(len(random_words)):
                if random_words[i] == ask:
                    space[i] = ask
                    print(space)
            repeat1 == True
        if ask in guessed_letters:
            print("already found")

        if "-" not in space:
            print("you won")
            quit(
                )
    if trials == 6:
        print(states[6])
    elif trials == 5:
        print(states[5])
    elif trials == 4:
        print(states[4])
    elif trials == 3:
        print(states[3])
    elif trials == 2:
        print(states[2])
    elif trials == 1:
        print(states[1])
    elif trials == 0:
        print(states[0])
        print("game over")
        running == False
        quit()
        
    
