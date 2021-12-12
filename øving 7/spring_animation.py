from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import time


time_interval = 0

# Initial values
position = 15
velocity = 0
acceleration = 0
sim_time = 0
simulation_time = 30.0

# Constants
mass = 2 # mass
k = 3 # spring coefficient
b = 0.1 # damping coefficient
# b = 2*np.sqrt(k*mass)# critical damping coefficient




class GraphPlot():
    def __init__(self,label, color):
        self.first_patch = plt.Polygon([[10, 10]], closed=None, fill=None, edgecolor=color, label=label)

    def init_func(self):
        self.first_patch.xy = [[0, 0]]
        return [self.first_patch]

    def update(self, data):
        # Add current x position to x graph
        arr = self.first_patch.get_xy().tolist()
        arr.append(data[0])
        self.first_patch.xy = arr

        return [self.first_patch]


def animate(i):
    global velocity,acceleration

    sim_time = time.time()  - start_time

    sim_time_label.set_text("Simulation Time: " + str(round(sim_time,2)))

    x, v,a = set(sim_time)





    X = np.linspace(x, 20, 1000)
    sinX = np.linspace(4 * np.pi, 6 * np.pi, 100)
    X3 = np.tile(sinX, 10)
    Y = 5*np.sin(X3)
    spring.set_data(X[:1000],Y[:1000])



    patch.xy = (x - 5, -1.25)
    acceleration_arrow.xy = a , 0
    acceleration_arrow.set_position([x,0])
    velocity_arrow.xy = v , 0
    velocity_arrow.set_position([x,0])

    pos_plot = plots[1].update([[sim_time, x], [sim_time,0]])
    vel_plot = plots[2].update([[sim_time, v], [sim_time,0]])
    acc_plot = plots[3].update([[sim_time, a],[sim_time,0]])
    ret_ = [patch, sim_time_label,spring, acceleration_arrow, velocity_arrow] + acc_plot + vel_plot + pos_plot

    return ret_


def init_func():
        sim_time_label.set_text("")
        patch.xy = (0, 0)

        pos_plot = plots[1].init_func()
        vel_plot = plots[2].init_func()
        acc_plot = plots[3].init_func()
        ret_ = [patch, sim_time_label] + acc_plot + vel_plot + pos_plot

        return ret_





def init_plots( plotx, ploty, xmin,xmax,ymin,ymax,xlabel, ylabel, title, color):
    ax[plotx,ploty].set_xlim((xmin, xmax))
    ax[plotx,ploty].set_ylim((ymin, ymax))
    plots.append(GraphPlot(title,color))
    ax[plotx,ploty].add_patch(plots[-1].first_patch)
    ax[plotx, ploty].set_xlabel(xlabel)
    ax[plotx, ploty].set_ylabel(ylabel)
    # ax[plotx, ploty].grid()
    ax[plotx, ploty].axhline(y=0, linewidth=0.7,color='k')
    # ax[plotx,ploty].legend()
    if plotx == 1 and ploty == 1:
        ax[plotx,ploty].add_patch(patch)

    ax[plotx,ploty].set_title(title)





def set(args):
    global position, velocity, acceleration, mass, k, b, time_interval # Get global variables

    dt = time.time() -  time_interval
    time_interval = time.time()
    spring_force = k * position # Fs = k * x
    damper_force = b * velocity # Fb = b * x'

    acceleration = - (spring_force + damper_force) / mass
    velocity += (acceleration * dt) # Integral(a) = v
    position += (velocity * dt) # Integral(v) = x

    return position, velocity, acceleration # Return position




if __name__ == "__main__":

    fig, ax = plt.subplots(2, 2, figsize=(13, 8))
    plt.subplots_adjust( hspace= 0.3)
    plots = [0]

    init_plots(0,0,0,simulation_time,-20, 20,"Time: (s)", "Position", "Position Plot", "g")

    init_plots(0,1,0,simulation_time,-20, 20,"Time: (s)", "Velocity ", "Velocity Plot","b")

    init_plots(1,0,0,simulation_time,-30, 30,"Time: (s)", "Acceleration" ,"Acceleration Plot", "r")

    sim_time_label = ax[1,1].text(0.03, 0.9, '', transform=ax[1,1].transAxes)
    acceleration_arrow = ax[1,1].annotate("", xy=(10000, 0), xytext=(0, 0), arrowprops={"facecolor": "r"})
    velocity_arrow = ax[1,1].annotate("", xy=(1000000, 0), xytext=(0, 0), arrowprops={"facecolor": "b"})


    X = np.linspace(position, 20, 1000)
    Y = 2.5*np.sin(position*X-position)

    spring, = plt.plot([0],[0], color="grey")
    patch = plt.Rectangle((0, -1.25), width=10, height=2.5, fc='tab:blue')
    start_time = time.time()
    time_interval = start_time
    init_plots(1,1,-20,20,-20, 20,"Y position", "X position", "Animation", None)
    animate = animation.FuncAnimation(fig, animate, interval=0.1, frames=30*60, blit=True, repeat=True, init_func=init_func)
    plt.show()
