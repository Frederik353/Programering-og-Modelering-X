import numpy as np
import matplotlib.pyplot as plt
# def f(x): return 1/(1 + x**2)


# def f(x): return x**4-3.5*x**3+5*x**2
def f(x): return np.sin(x)


a = 0
b = 30
N = 50

# x and y values for the trapezoid rule
x = np.linspace(a, b, N+1)
y = f(x)

# X and Y values for plotting y=f(x)
X = np.linspace(a, b, 1000)
Y = f(X)
# print(Y)
plt.plot(X, Y)

for i in range(N):
    xs = [x[i], x[i], x[i+1], x[i+1]]
    ys = [0, f(x[i]), f(x[i+1]), 0]
    plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2)

plt.title(f"Trapezoid Rule, N = {N}")
plt.show()
