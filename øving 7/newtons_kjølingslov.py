from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
# import csv

r = 0.0044
tEnv = -12
T = 27

y = [T]
x = np.linspace(-1, 10, 11*60)

for dt, val in enumerate(x[1:]):
    y.append(y[-1] + ( - r * (y[-1] - tEnv) * (dt / 60)))


data = []

with open("./temperature_10min.txt" , "r" ) as f:
    for element in f:
        data.append(int(element))
    data = np.array(data)

t = np.array(range(0, len(data)))/ 60

plt.figure(figsize=(15, 5))
plt.plot(t, data, c="red", label="Temperatur", linewidth=1)
plt.xlabel("Tid [min]", fontsize = 16)
plt.ylabel("Temperatur [\u00b0C]", fontsize = 16)
plt.title("Temperatur fall etter lagt i fryser", fontsize = 16)
plt.legend()
plt.tight_layout()
plt.savefig("Temperatureplot.png", dpi = 300)

plt.plot(x, y, '-b', label='Model', linewidth=1)
plt.legend(loc='best')
plt.grid(b=True, linewidth=0.5)
plt.show()


data = [['Time', 'Temperture']]
for row in range(len(x)):
    data.append([x[row],y[row]])


