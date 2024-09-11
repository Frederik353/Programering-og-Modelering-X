import matplotlib.pyplot as plt
import numpy as np


data = []

with open("./temperature_10min.txt", "r") as f:
    for element in f:
        data.append(int(element))
    data = np.array(data)


in_to_cm = 1/2.54

fig_size = 14 * np.array([1, 1/1.618]) * in_to_cm
t = np.array(range(0, len(data))) / 60

fig = plt.figure(dpi=300, figsize=fig_size)

plt.grid()


plt.plot(t, data, c="red", label="Temperatur")
plt.xlabel("Tid [min]", fontsize=16)
plt.ylabel("Temperatur [\u00b0C]", fontsize=16)
plt.title("Temperatur fall etter lagt i fryser", fontsize=16)
plt.legend()
plt.tight_layout()
plt.savefig("Temperatureplot.png", dpi=300)
plt.show()
