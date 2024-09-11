
from matplotlib import pyplot as plt
import numpy as np


def main():
    data = []
    with open("./random.txt" , "r" ) as f:
        for element in f:
            data.append(int(element))
    
    data = np.array(data)

    x = np.arange(len(data))
    fig, ax = plt.subplots(2, 2, figsize=(6, 4))

    fig.suptitle("tilfeldige tall")

    ax[0][0].plot(x, data, color='#00aaff')
    ax[0][0].set_title("Usortert")
    ax[0][0].set_ylabel("verdi")
    ax[0][0].set_xlabel("Input number")

    sorted = np.copy(data) # deep copy
    sorted.sort()
    ax[0][1].plot(x, sorted, color='#00aaff')
    ax[0][1].set_title("Sortert")
    ax[0][1].set_ylabel("verdi")
    ax[0][1].set_xlabel("Input number")

    multipleOfPi = np.copy(data) * np.pi # mulig pga numpy array
    ax[1][0].plot(x, multipleOfPi, color='#00aaff')
    ax[1][0].set_title("Multiplisert med pi")
    ax[1][0].set_ylabel("verdi")
    ax[1][0].set_xlabel("Input number")
    
    logarthmic = np.log(np.copy(data))
    logarthmic.sort()
    ax[1][1].plot(x, logarthmic, color='#00aaff', label='Naturlig logaritme')
    logarthmic = np.log10(np.copy(data))
    logarthmic.sort()
    ax[1][1].plot(x, logarthmic, color='#aa00ff', label='Briggsk logaritme')
    ax[1][1].set_title("Logaritmiske verdier")
    ax[1][1].set_ylabel("verdi")
    ax[1][1].set_xlabel("Input number")
    ax[1][1].legend()


    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()
    plt.show()



if __name__ == "__main__":
    main()