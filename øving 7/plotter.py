import matplotlib.pyplot as plt
import numpy as np


data = []

with open("./temperature_10min.txt", "r") as f:
    for element in f:
        data.append(int(element))
    data = np.array(data)


# in_to_cm = 1/2.54

# fig_size = 14 * np.array( [1, 1/1.618] ) * in_to_cm
t = np.array(range(0, len(data))) / 60

# fig = plt.figure(dpi = 300, figsize=fig_size)
fig = plt.figure(figsize=(15, 7))


# def make_system(T_init, volume, r, t_end):
#     return class System:


class coffee:
    T_init = 90
    T_final = T_init
    volume = 300
    r = 0.01
    t_end = 30
    T_env = 22
    t_0 = 0
    dt = 1

# _init__(self):
    #     self.T_init = 90
    #     self.T_final = self.T_init
    #     self.volume = 300
    #     self.r = 0.01
    #     self.t_end = 30
    #     self.T_env = 22
    #     self.t_0 = 0
    #     self.dt = 1

print(coffee.volume)

# coffee = make_system(T_init=90, volume=300, r=0.01, t_end=30)
# coffee.init()

def change_func(t, T, system):
    r, T_env, dt = system.r, system.T_env, system.dt
    return -r * (T - T_env) * dt


change_func(0, coffee.T_init, coffee)


def run_simulation(system, change_func):
    t_array = linrange(system.t_0, system.t_end, system.dt)
    n = len(t_array)

    series = TimeSeries(index=t_array)
    series.iloc[0] = system.T_init

    for i in range(n - 1):
        t = t_array[i]
        T = series.iloc[i]
        series.iloc[i + 1] = T + change_func(t, T, system)

    system.T_final = series.iloc[-1]
    return series


results = run_simulation(coffee, change_func)


show(results.head())

show(results.tail())

results.plot(label="coffee")

decorate(xlabel="Time (minute)", ylabel="Temperature (C)", title="Coffee Cooling")


coffee.T_final


plt.grid()

plt.plot(t, data, c="red", label="Temperatur")
plt.xlabel("Tid [min]", fontsize=16)
plt.ylabel("Temperatur [\u00b0C]", fontsize=16)
plt.title("Temperatur fall etter lagt i fryser", fontsize=16)
plt.legend()
plt.tight_layout()
# plt.savefig("Temperatureplot.png", dpi = 300)
plt.show()
