import random
import math

lower = int(input("nedre grense:"))
upper = int(input("øvre grense: "))

input_maks_antall_gjett = int(input("maks antall gjett: "))
print(input_maks_antall_gjett, (input_maks_antall_gjett == ""))
maks_antall_gjett = {round(math.log(upper - lower + 1, 2))} if input_maks_antall_gjett == 0 else input_maks_antall_gjett

x = random.randint(lower, upper)
print(f"du har bare {maks_antall_gjett} forsøk på å gjette tallet \n")

antall_gjett = 0

while antall_gjett < math.log(upper - lower, 2):
    antall_gjett += 1

    gjettet_tall = int(input("Gjett et tall: "))


    if x == gjettet_tall:
        print(f"Du gjettet riktig  etter {antall_gjett} forsøk")
        break
    elif x > gjettet_tall:
        print("Du gjettet for lavt")
    elif x < gjettet_tall:
        print("Du gjettet for høyt")


if antall_gjett >= math.log(upper - lower, 2):
    print(f"nummeret er {x}")
