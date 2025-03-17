import random

def word():
    w = ['Apple', 'Orange', 'Watermelon', 'Mango']
    return w

def getword():
    random_index = random.randint(0, 3)
    comp_word = word()
    C_word = comp_word[random_index].upper()
    return C_word

def display_hangman(tries):
    states = [
        """
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
        """
    ]
    return states[tries]

def play(word):
    _list = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    num_of_tries = 6

    print("Let's Play Hangman!")
    print(display_hangman(num_of_tries))
    print(" ".join(_list))  # Show underscores with spaces
    print("\n")

    while not guessed and num_of_tries > 0:
        guess = input("Please Guess a Letter or Word: ").upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                num_of_tries -= 1
                guessed_letters.append(guess)
            else:
                print("Great! The letter", guess, "is correct.")
                guessed_letters.append(guess)
                word_as_list = list(_list)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                _list = "".join(word_as_list)
                if "_" not in _list:
                    guessed = True

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                num_of_tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                _list = word  # Reveal the word

        else:
            print("Not a valid guess.")

        print(display_hangman(num_of_tries))
        print(" ".join(_list))  # Show progress with spaces
        print("\n")

    if guessed:
        print("Congratulations! You guessed the word correctly.")
    else:
        print("Game Over! The word was:", word)

words = getword()
play(words)

 

 

