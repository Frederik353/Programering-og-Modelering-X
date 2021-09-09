import random


liste = random.sample(range(100),100)

print(liste)

ALDERSGRUPPER = [("undefined",17),(18,67),(67,"undefined")] # tuple (fra og med, til og med)

def antall_i_aldersgruppe(ALDERSGRUPPER, liste):
    grupper_info = []
    for ALDERSGRUPPE in ALDERSGRUPPER:
        if ALDERSGRUPPE[0] == "undefined":
            if ALDERSGRUPPE[1] == "undefined":
                antall_i_gruppe = len(liste)
                aldersgruppe_string = "har en alder"
            else:
                antall_i_gruppe = len([0 for j in liste if j < ALDERSGRUPPE[1]])
                aldersgruppe_string = f"under {ALDERSGRUPPE[1] + 1}år"
        elif ALDERSGRUPPE[1] == "undefined":
            antall_i_gruppe = len([1 for j in liste if j > ALDERSGRUPPE[0]])
            aldersgruppe_string = f"{ALDERSGRUPPE[0]}år og over"
        else:
            antall_i_gruppe =  len([1 for j in liste if j < ALDERSGRUPPE[1]]) - len([1 for j in liste if j < ALDERSGRUPPE[0]])
            aldersgruppe_string = f"mellom {ALDERSGRUPPE[0]} og {ALDERSGRUPPE[1]}år"
        grupper_info.append([antall_i_gruppe, aldersgruppe_string])
    return grupper_info


grupper_info = antall_i_aldersgruppe(ALDERSGRUPPER, liste)

for i in grupper_info:
    print(f"Det er {i[0]} personer som er i aldersgruppen {i[1]}")
