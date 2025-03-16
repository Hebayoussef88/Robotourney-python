def display_contacts(contacts):
    if not contacts:
        print("\nYour contact list is empty.")
    else:
        print("\nContact List:")
        print("-" * 25)
        for name, number in contacts.items():
            print(f"{name}: {number}")
        print("-" * 25)

def add_contact(contacts):
    name = input("Enter contact name: ")
    number = input("Enter phone number: ")
    if name in contacts:
        print("This contact already exists!")
    else:
        contacts[name] = number
        print(f"{name} added successfully!")

def search_contact(contacts):
    name = input("Enter name to search: ")
    if name in contacts:
        print(f"{name}: {contacts[name]}")
    else:
        print("Contact not found!")

def delete_contact(contacts):
    name = input("Enter name to delete: ")
    if name in contacts:
        del contacts[name]
        print(f"{name} deleted successfully!")
    else:
        print("Contact not found!")

def main():
    contacts = {}
    while True:
        print("\n1. Add Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. Display Contacts")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            delete_contact(contacts)
        elif choice == "4":
            display_contacts(contacts)
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()