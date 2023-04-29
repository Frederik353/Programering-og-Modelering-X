import random
import numpy as np
import mmap


# laaget også en multi threaded verson av denne oppgaven som delte opp filen og ga en del av filen til en thread før jeg kom på at python gil (Global interpreter lock) gjør att dette var helt meningsløst, (skrevet en del rust i det siste hvor dette er mulig og ville i såfall gitt nesten 4x hastighet pga 4 kjerner i cpuen, ingen hyperthreading)

def kuponger(antall, fil):
    with open(fil, "w") as f:
        for i in range(antall):
            kupong = random.sample(range(35), 7)
            f.write(" ".join(map(str, kupong)))
            f.write("\n")


def antallRette(kupong, trekning):
    ekstra = 1 if trekning[-1] in kupong else 0
    like = set(kupong) & set(trekning)
    return [len(like) - ekstra, ekstra]


def antallpremier(fil):
    vinnere = np.zeros(6)
    with open(fil, "r+b") as f:
        # memmory mapper filen in i ram, minker system calls, offrer lagring for tid, hjelper ikke veldig mye i denne situasonen men vil trolig hjelpe mere hvis man skal åpne flere filer
        map_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(map_file.readline, b""):
            kupong = line.decode("utf-8").split(" ")
            kupong = list(map(int, kupong))
            rette = antallRette(kupong, [1, 2, 3, 4, 5, 6, 7, 8])
            # på grunn av negativ eksponentiell vekst er det viktig å sjekke de med minst riktige først ettersom dette er den største gruppen og de andre gruppene vil være statistiske ubetydelige for kjøre tiden
            if rette[0] < 3:
                vinnere[0] += 1
            elif rette[0] < 6:
                vinnere[rette[0] - 3] += 1
            elif rette[0] == 6:
                if rette[1] == 1:
                    vinnere[4] += 1
                else:
                    vinnere[3] += 1
            else:
                vinnere[5] += 1
    return vinnere


def inntjening(vinnere, antall):
    intjening = 0
    premier = [0, 50, 110, 4_500, 100_000, 2_500_000]
    utbetalt = []
    for num1, num2 in zip(vinnere, premier):
        utbetalt.append(num1 * num2)
    sumUtbetalt = sum(utbetalt)
    fortjeneste = (antall * 10) - sumUtbetalt
    return fortjeneste, sumUtbetalt, utbetalt


np.set_printoptions(suppress=True)  # hindrer vitenskapelig notasjon


def main():
    antall = 10_000_000
    kuponger(antall, "./kuponger.txt")
    vinnere = antallpremier("./kuponger.txt")
    fortjeneste, sumUtbetalt, utbetalt = inntjening(vinnere, antall)
    print(vinnere)
    print(utbetalt)
    print("------------------------------------------------------------------------")
    print(f"Norsk Tipping tjente {fortjeneste}kr denne trekning.")
    print(
        f"Totalt ble {antall} kuponger levert, hvor {vinnere[-1]} vant første premien.")


if __name__ == "__main__":
    main()
