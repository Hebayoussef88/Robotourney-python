import random

def choose_word():
    words = ["python", "hangman", "programming", "developer", "computer"]
    return random.choice(words)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def play_game():
    word = choose_word()
    guessed_letters = set()
    attempts = 6
    print("welcome to hangman")

    while attempts > 0:
        print(display_word(word, guessed_letters))
        guess = input("guess a letter ")

        if guess in guessed_letters:
            print("you already guessed that letter")
        elif guess in word:
            guessed_letters.add(guess)
            print("correct")
            if set(word) == guessed_letters:
                print("congrats you guess this word", word)
                
        else:
            guessed_letters.add(guess)
            attempts -= 1
            print("incorrect attempts remaining", attempts)

        if attempts == 0:
            print("game over the word was", word)

play_game()
