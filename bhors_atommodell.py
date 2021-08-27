BOHRS_KONSTANT = 2.18 * 10**-18

fra_nivå = int(input("fra nivå?"))
til_nivå = int(input("til nivå"))

def energiUtløst(fra_nivå, til_nivå = 1): 
    Energi = -( BOHRS_KONSTANT / fra_nivå**2) + ( BOHRS_KONSTANT / til_nivå**2)
    return Energi


LYS_FART = 3* 10**8
PLANKS_KONSTANT = 4.14 * 10**-15 

def lysEmmitert(Energi):
    frekvens = Energi / PLANKS_KONSTANT
    bølgelengde = (PLANKS_KONSTANT * LYS_FART) / Energi
    return frekvens, bølgelengde


frekvens, bølgelengde = lysEmmitert(energiUtløst(fra_nivå, til_nivå))
print(frekvens,bølgelengde)
if frekvens < 700*10^-9:
    print("ultrafiolett")
elif frekvens < 625* 10**-9:
    print("infrarødt")
else: 
    print("synelig lys")