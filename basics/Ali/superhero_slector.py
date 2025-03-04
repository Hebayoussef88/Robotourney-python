#superhero vs. villain selector
print("--------------------superhero vs. villain selector--------------------")
import math
import random
superheroes = ["superman", "batman", "deadpool", "wolverine"]
print(f"the superheroes are {superheroes}")
villans = ["Joker", "Jaugernaut", "sabertooth", "lex luthor"]
print(f"and the villians are {villans}")
question = int(input("how many matches? "))
for i in range(question):
    print("the match will be")
    a = random.choice(superheroes)
    b = random.choice(villans)
    y = (f"{a} will go against {b}")
    print(y)