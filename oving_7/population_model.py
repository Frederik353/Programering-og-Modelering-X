import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

var = pd.read_excel("./UN_world_population_data.xlsx", header=16)

x = list(var.loc[:, "1950":"2100"])
x = list(map(int, x))
un_y = var.iloc[0, 7:160]
un_y = list(map(int, un_y))


def logistic_model(t_0, t_end, L, k, forskyvining):
    results = [p_0]
    print(type(results))
    a = 0
    b = a + 150
    for t in range(a, b):
        results.append((L) / (1 + forkyvining * math.e**(-k * (t))))
    return results


# L =  10875394
L = 11_500_000
k = 0.03
forskyvning = 3.8

model_y = logistic_model(x[0], 2100, L, k, forskyvning)

n = np.linspace(0, 10, 10)
fig, ax = plt.subplots(figsize=(15, 8))

plt.plot(x, model_y, c="b", label="Model Prediction")
plt.plot(x[:72], un_y[:72], c="red", label="UN Data", linewidth=1)
plt.plot(x[71:],
         un_y[71:],
         c="y",
         linestyle="dashed",
         label="UN prediction",
         linewidth=1)
ax.ticklabel_format(style='plain')
plt.legend(loc="best")
plt.xlabel("Year")
plt.ylabel("Population")
plt.locator_params(axis="x", nbins=20)
plt.locator_params(axis="y", nbins=10)
plt.grid()
plt.title("Logistic World Population model")
plt.show()
