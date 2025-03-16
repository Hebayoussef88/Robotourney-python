# Tuple of available items in stock
available_items = ("apple", "banana", "orange", "grape", "mango", "pear")

# List to store cart items
cart = []

def add_to_cart(item):
    if item in available_items:
        cart.append(item)
        print(f"{item} added to cart.")
    else:
        print(f"Sorry, {item} is not available.")

def remove_from_cart(item):
    if item in cart:
        cart.remove(item)
        print(f"{item} removed from cart.")
    else:
        print(f"{item} is not in the cart.")

def view_cart():
    if cart:
        print("Your cart contains:", ", ".join(cart))
    else:
        print("Your cart is empty.")

def total_items():
    print(f"Total items in cart: {len(cart)}")

def check_availability(item):
    if item in available_items:
        print(f"{item} is available.")
    else:
        print(f"{item} is not available.")

# Sample interaction
while True:
    print("\nOptions: add, remove, view, total, check, exit")
    action = input("Enter your choice: ").strip().lower()
    
    if action == "add":
        item = input("Enter item to add: ").strip().lower()
        add_to_cart(item)
    elif action == "remove":
        item = input("Enter item to remove: ").strip().lower()
        remove_from_cart(item)
    elif action == "view":
        view_cart()
    elif action == "total":
        total_items()
    elif action == "check":
        item = input("Enter item to check: ").strip().lower()
        check_availability(item)
    elif action == "exit":
        print("Thank you for shopping!")
        break
    else:
        print("Invalid option, please try again.")