import random


liste = random.sample(range(5),5)

# i en produksjons kode ville sum() funksjonen vert den beste løsning


def sum_list(liste):
    sum  = 0
    for n in liste:
        sum += n
    return sum

print(liste)
print(sum_list(liste))
print(sum(liste)) # test