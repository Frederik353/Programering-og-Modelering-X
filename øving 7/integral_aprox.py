
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate


# def f(x): return 1/(1+x**2)
def f(x): return np.sin(x)


a = 0
b = 2*np.pi
N = 10
n = 100  # Use n*N+1 points to plot the function smoothly
dx = (b - a)/N

x = np.linspace(a, b, N+1)
y = f(x)

X = np.linspace(a, b, n*N+1)
Y = f(X)

plt.style.use("dark_background")
plt.rcParams['font.size'] = 8
plt.figure(figsize=(13, 9))



# finner integral å teste opp mot
area = integrate.quad(f, a, b)
print(f" area: { round(area[0],5) }, error: {area[1] }")


def sum_area(y_vals):
    return round(np.sum(y_vals) * N / (b - a), 2)


def sum_under(plot, graphX, graphY, barX, barY):
    plt.subplot(2, 4, plot)  # velger plot
    # plt.grid()
    plt.plot(graphX, graphY, 'b')  # plotter graf
    # plotter punk hvor høyden på bokesne blir bestemt
    plt.plot(barX, barY, 'b.', markersize=10)
    # plotter bokser
    if plot == 1:  # left
        plt.bar(barX, barY, width=dx, alpha=0.2,
                align='edge', edgecolor='b')
    elif plot == 2:  # midpoint
        plt.bar(barX, barY, width=dx, alpha=0.2, edgecolor='b')
    elif plot == 3:  # right
        plt.bar(barX, barY, width=-dx, alpha=0.2,
                align='edge', edgecolor='b')
    return sum_area(barY)


def riemann_sum(upper):
    sum_array = []
    prev = x[0]
    for i in x[1:]:
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


# Right
x_left = x[:-1]
y_left = y[:-1]
sum = sum_under(1, X, Y, x_left, y_left)
plt.title(f"Left Riemann Sum, N = {N}, A = {sum}")

# Midpoint
x_mid = (x[:-1] + x[1:])/2
y_mid = f(x_mid)
sum = sum_under(2, X, Y, x_mid, y_mid)
plt.title(f"Midpoint Riemann Sum, N = {N}, A = {sum}")

# Left
x_right = x[1:]
y_right = y[1:]
sum = sum_under(3, X, Y, x_right, y_right)
plt.title(f"Left Riemann Sum, N = {N}, A = {sum}")


# lower
sum_under(4, X, Y, x_right, y_right)
sum = riemann_sum(False)
plt.title(f"Lower Riemann Sum, N = {N}, A = {sum}")

# upper
sum_under(5, X, Y, x_right, y_right)
sum = riemann_sum(True)
plt.title(f"Upper Riemann Sum, N = {N}, A = {sum}")

# Trapezoidal
sum_under(6, X, Y, [], [])

for i in range(N):
    xs = [x[i], x[i], x[i+1], x[i+1]]
    ys = [0, f(x[i]), f(x[i+1]), 0]
    plt.fill(xs, ys, 'b', edgecolor='b', color="tab:blue", alpha=0.2)
    plt.plot(xs[1], ys[1], 'b.', markersize=10)

sum = round((dx/2) * np.sum(y[1:] + y[:-1]), 2)
plt.title(f"Trapezoid Rule, N = {N}, A = {sum}")


# simpsons rule
def p(x, a, b, c): return (a*(x**2))+(b*x)+c


sum_under(7, X, Y, [], [])


def simps(x, y):
    print(N)
    if N % 2 == 1:
        raise ValueError("N must be an even integer.")
    A = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])

    points = np.column_stack((x, y))
    prev = points[0]
    for current in points[1:]:
        p1 = prev
        midpointX = current[0] - (dx/2)
        p2 = [midpointX, f(midpointX)]
        p3 = current
        a, b, c = calc_parabola_vertex(p1, p2, p3)

        x_pos = np.linspace(current[0],  prev[0], n+1)
        y_pos = p(x_pos, a, b, c)

        plt.plot(x_pos, y_pos, "b")  # parabola line
        plt.fill_between(x_pos, y_pos, color="tab:blue", alpha=0.2)
        # plt.scatter(x_pos, y_pos, color='gray')  # parabola points
        # plt.scatter(p1[0], p1[1], color='r', marker="D", s=50)  # 1st known xy
        plt.scatter(p2[0], p2[1], color='g', marker="D", s=50)  # 2nd known xy
        # plt.scatter(p3[0], p3[1], color='k', marker="D", s=50)  # 3rd known xy
        prev = current

    return A


def calc_parabola_vertex(p1, p2, p3):
    denom = (p1[0]-p2[0]) * (p1[0]-p3[0]) * (p2[0]-p3[0])
    A = (p3[0] * (p2[1]-p1[1]) + p2[0] *
         (p1[1]-p3[1]) + p1[0] * (p3[1]-p2[1])) / denom
    B = ((p3[0]**2) * (p1[1]-p2[1]) + (p2[0]**2) *
         (p3[1]-p1[1]) + (p1[0]**2) * (p2[1]-p3[1])) / denom
    C = (p2[0] * p3[0] * (p2[0]-p3[0]) * p1[1]+p3[0] * p1[0] *
         (p3[0]-p1[0]) * p2[1]+p1[0] * p2[0] * (p1[0]-p2[0]) * p3[1]) / denom
    return A, B, C


sum = round(simps(x, y), 3)
plt.title(f"Simpsons rule, N = {N}, A = {sum}")

plt.show()
