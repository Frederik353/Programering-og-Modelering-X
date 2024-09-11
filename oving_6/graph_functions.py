import numpy as np
from matplotlib import pyplot as plt

# f(x)= 3x^2+ 7x − 3 og g(x)=x^3−2x+1 i Python.

# B) Finn f(5), g(7), f(3)⋅g(2)  og f(g(3)).


def f(x):
    return (3 * (x**2) + (7 * x) - 3)


def g(x):
    return x**3 - 2 * x + 1


def main():
    print(f"f(5) er {f(5)}")
    print(f"g(7) er {g(7)}")
    print(f"f(3) x g(2) er {f(3) * g(2)}")
    print(f"f(g(3) er {f(g(3))}")
    print(f"")

    x = np.arange(-5, 5, 0.01)
    fgraf = []
    ggraf = []
    fggraf = []
    favggraf = []
    for xval in x:
        fgraf.append(f(xval))
        ggraf.append(g(xval))
        fggraf.append(f(xval) * g(xval))
        favggraf.append(f(g(xval)))

    fgraf = np.array(fgraf)
    fig = plt.figure(figsize=(17, 7))
    fig.suptitle("grafer")

    plt.plot(x, fgraf, color='#00aaff')
    plt.plot(x, ggraf, color='#00aaff')
    plt.plot(x, fggraf, color='#00aaff')
    plt.plot(x, favggraf, color='#00aaff')
    plt.ylabel("y-akse")
    plt.xlabel("x-akse")
    plt.show()


if __name__ == "__main__":
    main()
