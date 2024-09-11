import math



"""
    antar at n er et posetiv naturlig tall
    tids kompleks O(sqrt(n)) hvor n er input tallet
"""




# for i in range(1, 11):
#     state = "et primtall" if er_primtall(i) else "ikke et primtall"
#     print(f"{i} er {state}" )


def primtalls_faktorer(n):
    faktorer = []
    while n % 2 == 0: # while n er oddetall
        faktorer.append(2)
        n = n / 2

    for i in range(3 , int(math.sqrt(n)) + 1 , 2): # looper over oddetall fra 3 opp til heltall kvadratroten av n
        while (n % i == 0):
            faktorer.append(i)
            n = n / i

    if n > 2:
        faktorer.append(i)
    return faktorer

n = int(input("Finn primtallsfaktorer for:"))
primtalls_faktorer(n)