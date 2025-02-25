

def add_contact(contacts):
    name = input("Enter  name: ")
    phone = input("Enter  phone number: ")
    contacts[name]= phone
    print(f"{name} was successfully")

def remove_contact(contacts):
    name1 = input("Enter name: ")
    if name1 in contacts:
        del contacts[name1]
        print(f"{name1}succusfully deleted")
    else:
        print("sorry name doesnt exist in contacts")

def view_contact(contacts):
    print(contacts)

def search_contacts (contacts):
    name2 = input("Enter the name of the contact you are looking for: ")
    if name2 in contacts:
        print(f"{name2}'s phone number is {contacts[name2]}")
    else:
        print(f"No contact found with the name {name2}")

def main():
    contacts = {}
    while True:
       print("1. add new contact")
       print("2. remove contact")
       print("3. search for contact")
       print("4. view all contacts")
       print("5. exit")
       choice = input("choose a number")

    
       if choice == "1":
              add_contact(contacts)
       elif choice == "2":
             search_contacts(contacts)
       elif choice == "3":
              remove_contact(contacts)
       elif choice == "4":
              view_contact(contacts)
       elif choice == "5":
              break
       else:
              print("invaild choice try again")

main()
