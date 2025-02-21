
correct_pin = "4321"  
attempts = 3  

while attempts > 0:
    pin = input("Enter your 4-digit ATM PIN: ") 
    if pin == correct_pin:
        print("✅ Access granted! Welcome to your account.")
        break
    else:
        attempts -= 1  
        if attempts == 0:
            print("❌ Too many failed attempts. Your account is locked.")
        else:
            print(f"❌ Incorrect PIN. You have {attempts} attempt(s) left.")
