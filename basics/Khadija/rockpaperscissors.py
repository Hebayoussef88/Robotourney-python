import random

user_score = 0
computer_score = 0

def computer_choice():
    choices = ["Rock", "Paper", "Scissors"]
    return random.choice(choices)

def calculate_Result(user, computer):
    global user_score
    global computer_score

    if (user == "Rock" and computer == "Scissors") or \
       (user == "Scissors" and computer == "Paper") or \
       (user == "Paper" and computer == "Rock"):
        user_score += 1
        result = "You Win"
    elif user == computer:
        result = "Draw"
    else:
        computer_score += 1
        result = "You Lose"

    return user_score, computer_score, result

while True:
    print('''
          1 - Rock
          2 - Paper
          3 - Scissors
    ''')

    comp_ch = computer_choice()
    user_input = input("Enter Your Choice (Rock, Paper, Scissors): ").capitalize()

    if user_input not in ["Rock", "Paper", "Scissors"]:
        print("Invalid input! Please enter Rock, Paper, or Scissors.")
        continue

    user_sc, com_sco, result = calculate_Result(user_input, comp_ch)

    print(f"Computer chose: {comp_ch}")
    print(f"The Score of Computer: {com_sco} | The User Score: {user_sc}")
    print(f"The Result of This Round: {result}")

