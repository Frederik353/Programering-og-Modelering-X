import random


"""
    det raskeste og beste er igjen å ikke gjøre det selv å heller bruke den innebygde min() funksjonen
    kan også sortere listen med sort(), da vill de minste talle være på index 0 og største på -1
"""

liste = random.sample(range(10000000),10000000)


def minste_tall(liste):
    min = liste[0]
    for index ,num in enumerate(liste):
        if min > num:
            min = num
            min_index = index
    return min, min_index


# def minste_tall(liste):
#     min = liste[0]
#     for i in range(len(liste)):
#         if min > liste[i]:
#             min = liste[i]
#             min_index = i
#     return min, min_index

print(liste)
print(minste_tall(liste))

