

from matplotlib import pyplot as plt
import numpy as np


def collatz_conjecture(n):
    graf = []
    while n > 1:
        graf.append(n)
        if (n % 2):
            n = 3*n + 1
        else:
            n = n//2
        #kan skrives som ( n = n / 2 if n % 2 == 0 else n*3 + 1 ) med en ternary operator men er litt vanskeligere å lese
    return graf


def color_picker():
    return np.random.choice(["#167df3", "#0ab6ff", "#0affe7", "#89bbfe", "#4775ff", "#515190", "#cbd5f6"])


def transforms(x):
    seq = [0]
    val = [0]
    rad = 0
    even = -.54 * (np.pi / 180)
    odd = 1.2 * (np.pi / 180)
    for i in range(1, len(x)):
        if x[i] % 2 == 0:
            seq.append(seq[i-1]+np.sin(rad+even))
            rad = rad+even
        else:
            seq.append(seq[i-1]+np.sin(rad+odd))
            rad = rad+odd
        val.append(val[i-1]+np.cos(rad))
    return val, seq


def main():

    # for i in range(2,50):
    #     print(f"{i} ->  {collatz_conjecture(i)})

    x = np.arange(1000)
    grafer = [collatz_conjecture(i) for i in x]
    y = [len(i) for i in grafer]

    plt.style.use("dark_background")
    fig, ax = plt.subplots(3, 1, figsize=(6, 4))

    fig.suptitle("collatz-conjecture")

    ax[0].scatter(x, y, color='#00aaff', marker='.')
    ax[0].set_title("Number of steps to finish")
    ax[0].set_ylabel("Number of steps to finish")
    ax[0].set_xlabel("Input number")

    sequence_lengths = []
    for i in range(len(x)):
        x_akse = np.arange(len(grafer[i]))
        ax[1].plot(x_akse, grafer[i], label=i)
        fig.set_figheight(10)
        fig.set_figwidth(10)
        length = collatz_conjecture(i)
        sequence_lengths.append(length)
        x, y = transforms(np.array(length))
        ax[2].set_facecolor('black')
        ax[2].plot(x, y, alpha=0.15, color=color_picker())

    ax[1].set_ylabel("value")
    ax[1].set_xlabel("steps")

    plt.show()


if __name__ == "__main__":
    main()
