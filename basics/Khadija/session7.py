import random

def say_hero():
    heroes = ["Supernova", "Shadow Hawk", "Blaze Phantom", "Iron Titan", "Storm Striker"]
    return random.choice(heroes)

def say_enemy():
    enemies = ["Dark Specter", "Venom Claw", "Nightmare King", "Cyber Reaper", "Inferno Doom"]
    return random.choice(enemies)

def main():
    hero = say_hero()
    enemy = say_enemy()
    print(f"The chosen hero is: {hero}")
    print(f"The enemy they will face is: {enemy}")

main()
