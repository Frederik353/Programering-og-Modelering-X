import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# def f(x): return 1/(1+x**2)


def f(x): return np.sin(x)


a = 0
b = 2*np.pi
N = 50
n = 10000  # Use n*N+1 points to plot the function smoothly

area = integrate.quad(f, a, b)
print(f" area: { area[0] }, error: {area[1]}")


def sum_area(y_vals):
    return round(np.sum(y_vals) * N / (b - a), 2)


x = np.linspace(a, b, N+1)
y = f(x)

X = np.linspace(a, b, n*N+1)
Y = f(X)

plt.figure(figsize=(15, 5))

plt.subplot(2, 3, 1)
plt.plot(X, Y, 'b')
x_left = x[:-1]  # Left endpoints
y_left = y[:-1]
plt.plot(x_left, y_left, 'b.', markersize=10)
plt.bar(x_left, y_left, width=(b-a)/N, alpha=0.2, align='edge', edgecolor='b')
left = sum_area(y_left)
plt.title(f"Left Riemann Sum, N = {N}, A = {left}")

plt.subplot(2, 3, 2)
plt.plot(X, Y, 'b')
x_mid = (x[:-1] + x[1:])/2  # Midpoints
y_mid = f(x_mid)
plt.plot(x_mid, y_mid, 'b.', markersize=10)
plt.bar(x_mid, y_mid, width=(b-a)/N, alpha=0.2, edgecolor='b')
mid = sum_area(y_mid)
plt.title(f"Midpoint Riemann Sum, N = {N}, A = {mid}")

plt.subplot(2, 3, 3)
plt.plot(X, Y, 'b')
x_right = x[1:]  # Left endpoints
y_right = y[1:]
plt.plot(x_right, y_right, 'b.', markersize=10)
plt.bar(x_right, y_right, width=-(b-a)/N,
        alpha=0.2, align='edge', edgecolor='b')
right = sum_area(y_right)
plt.title(f"Right Riemann Sum, N = {N}, A = {right}")

# lower


def reigenvalue(upper):
    sum_array = []
    prev = x[0]
    for i in x[1:]:
        # print(f(prev), f(i), f(i) > f(prev))
        if (f(i) > f(prev)) == upper:  # XNOR gate
            plt.bar(i, f(i), width=-(b-a)/N,
                    alpha=0.2, align='edge', edgecolor='b', color="tab:blue")
            plt.plot(i, f(i), 'b.', markersize=10)
            sum_array.append(f(i))
        else:
            plt.bar(prev, f(prev), width=(b-a)/N,
                    alpha=0.2, align='edge', edgecolor='b', color="tab:blue")
            plt.plot(prev, f(prev), 'b.', markersize=10)
            sum_array.append(f(prev))
        prev = i
    return sum_area(sum_array)


# lower
plt.subplot(2, 3, 4)
plt.plot(X, Y, 'b')
lower = reigenvalue(False)
plt.title(f"Lower Riemann Sum, N = {N}, A = {lower}")
# upper
plt.subplot(2, 3, 5)
plt.plot(X, Y, 'b')
upper = reigenvalue(True)
plt.title(f"Upper Riemann Sum, N = {N}, A = {upper}")


# zero_crossings = np.where(np.diff(np.sign(f(x))))[0]
# for zero_index in zero_crossings:
#     for index, xval in enumerate(x):
#         while index > zero_index:
#             # plt.plot(x_right, y_right, 'b.', markersize=10)
#             plt.bar(x_right, y_right, width=-(b-a)/N,
#                 alpha=0.2, align='edge', edgecolor='b')


# zero_crossings = np.where(np.diff(np.sign(Y)))[0]
# print(zero_crossings)
# plt.plot(x[zero_crossings], y[zero_crossings], 'ro')
# plt.plot(X[zero_crossings], Y[zero_crossings], 'ro')


plt.subplot(2, 3, 6)
# x and y values for the trapezoid rule
x = np.linspace(a, b, N+1)
y = f(x)

# X and Y values for plotting y=f(x)
# X = np.linspace(a, b, 1000)
# Y = f(X)
# print(Y)
plt.plot(X, Y)

for i in range(N):
    xs = [x[i], x[i], x[i+1], x[i+1]]
    ys = [0, f(x[i]), f(x[i+1]), 0]
    # print(xs, ys)
    # print(xs[1], ys[1])
    plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2)
    plt.plot(xs[1], ys[1], 'b.', markersize=10)


def trapz():
    y_right = y[1:]  # right endpoints
    y_left = y[:-1]  # left endpoints
    dx = (b - a)/N
    return (dx/2) * np.sum(y_right + y_left)


trap = trapz()


plt.title(f"Trapezoid Rule, N = {N}, A = {trap}")
plt.show()
