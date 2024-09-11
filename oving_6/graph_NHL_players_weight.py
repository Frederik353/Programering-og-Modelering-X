
from matplotlib import pyplot as plt
import numpy as np
import statistics

LBS_TO_KG = 0.45359237


def main():
    vektlbs = []
    with open("./vekt.txt", "r") as f:
        for element in f:
            vektlbs.append(int(element))

    vektlbs = np.array(vektlbs)
    vektkg = np.around(np.copy(vektlbs) * LBS_TO_KG)

    print(f"Vekten til {len(vektlbs)} spillere har blitt registrert. ")
    print(f"Snitt vekten er {sum(vektlbs) // len(vektlbs)} pund og {( sum(vektlbs) // len(vektlbs) ) * LBS_TO_KG} kilo.")
    print(f"Median vekten er {statistics.median(vektkg)} kg.")

    vektkg.sort()
    print(f"Den letteste spilleren veier {vektkg[0]} kg, og den tyngste spilleren veier {vektkg[-1]} kg.")
    x = np.arange(vektkg[0],vektkg[-1] + 1)
    y = np.zeros(len(x))

    offset = -vektkg[0]
    for vekt in vektkg:
        print(vekt + offset)
        y[int(vekt + offset)] += 1
    print(y) 
    fig = plt.figure(figsize=(17,7))
    fig.suptitle("Vekt til NHL spillere")
    plt.xticks(x)
    plt.yticks(np.arange(0,vektkg[0]))
    plt.bar(x, y, color='#00aaff')
    plt.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
    plt.ylabel("antall spillere")
    plt.xlabel("vekt [lbs]")
    plt.show()


if __name__ == "__main__":
    main()
