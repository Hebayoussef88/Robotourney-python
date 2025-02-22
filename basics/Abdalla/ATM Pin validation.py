password = "4243"
attempts = 0
max_attempts  = 3
while attempts < max_attempts:
    answer = input("enter your 4 digit pin:  ")
    if answer == password:
        print("correct password accses granted")
        break
    else:
       attempts += 1
       print(f"incorrect password you have {max_attempts-attempts} attempts left")
    if attempts == max_attempts:
       print("sorry the system is locked too many attempts")
      

    
