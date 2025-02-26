import random
enemy = ["blue man","grumpy","syntax error"]
hero = ["captin python","function man"]
def say_enemy(enemy):
    selected_enemy = random.choice(enemy)
    print(f"the enemy is {selected_enemy}")

def say_hero(hero):
    selected_hero = random.choice(hero)
    print(f"the hero is {selected_hero}")

say_enemy(enemy)
say_hero(hero)
