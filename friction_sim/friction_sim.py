import colorsys
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

# particle class stores all information about the particle


class Object:
    def __init__(self, name, color, size, p, v0, mu):
        global E
        # Initial values
        self.name = name
        self.color = color
        self.size = size
        self.mu = mu

        self.p = p          # position
        self.v0 = v0          # velocity
        self.v = v0          # velocity
        self.a = 0  # acceleration

        # arrays for saving state and graph
        self.pos_data = [self.p]
        self.vel_data = [self.v]
        self.acc_data = [self.a]

    def update(self, dt):
        F_friction = -np.sign(self.v) * self.mu * 9.8  # force due to friction
        F_net = F_friction

        # Calculate the object's acceleration
        self.a = F_net

        # Update the object's velocity and position
        self.v = self.v + self.a * dt
        self.p = self.p + self.v * dt

        # hindrer box fra å sprette frem og tilbake som konsekvens av ikke uendelige tidssteg
        if self.v < 0.01:
            self.v = 0

        # x(t) = x(0) + v(0)t - (1/2)μg*t^2

        # p = (v-1/2 * mu) *dt

        self.logstate()

        self.box.xy = [self.p, 0]
        self.acceleration_arrow.xy = self.p + self.a, 0.1
        self.acceleration_arrow.set_position([self.p + 0.15, 0.1])
        self.velocity_arrow.xy = self.p + self.v, 0.1
        self.velocity_arrow.set_position([self.p + 0.15, 0.1])
        return [self.box]

    def logstate(self):
        # saves the current state for plotting
        self.pos_data.append(self.p)
        self.vel_data.append(self.v)
        self.acc_data.append(self.a)


class Plot:

    def __init__(self, pos, plot, title, axeslabels, limits):

        self.pos = pos  # used to specify what is to be plotted
        self.title = title
        self.plot = plot
        self.axeslabels = axeslabels
        self.limits = limits

        self.plot.set_title(self.title)

        self.plot.set_xlim((self.limits[0][0], self.limits[0][1]))
        self.plot.set_ylim((self.limits[1][0], self.limits[1][1]))

        self.plot.set_xlabel(self.axeslabels[0])
        self.plot.set_ylabel(self.axeslabels[1])

        # self.plot.grid()


class friction_animation(Plot):

    annotations = []

    def __init__(self, pos, system, gridpos, title, axislabels, limits):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.plot.axhline(y=0, linewidth=0.7, color='w')

        # create boxes as representation for ice skates
        for o in self.system.objects:
            color = "#0000ff"
            label = 1
            o.acceleration_arrow = self.plot.annotate(
                "", xy=(10, 0), xytext=(0, 0), arrowprops={"edgecolor": "b", "facecolor": "b", "headlength": 6, "headwidth": 4, "width": 2})
            o.velocity_arrow = self.plot.annotate(
                "", xy=(10, 0), xytext=(0, 0), arrowprops={"edgecolor": "r", "facecolor": "r", "headlength": 6, "headwidth": 4, "width": 2})

            o.box = plt.Rectangle((0, 0), width=0.3, height=0.2, fc=o.color)
            self.plot.add_patch(o.box)

    def reframe(self):
        # makes sure all the data being displayd is within the plot

        # x
        min_x = float("inf")
        max_x = float("-inf")
        for o in self.system.objects:

            min_x = min(min_x, o.p)
            max_x = max(max_x, o.p)
        self.limits[0][0] = min_x
        self.limits[0][1] = max_x

        border = 3
        self.plot.set_xlim(
            (self.limits[0][0] - border, self.limits[0][1] + border))

    def update(self, xaxis, datasets):

        # self.plot.legend(loc=1, prop={'size': 8})
        self.reframe()
        for ann in self.annotations:
            ann.remove()
        self.annotations.clear()

        for o in self.system.objects:
            ann = self.plot.annotate(f"v0 {np.round(o.v0, 2)}", (o.p, -0.125), fontsize=7,
                                     bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.8))
            self.annotations.append(ann)

        ret_ = [self.plot]
        return ret_


class Plot3D(Plot):

    # rotation speed on 3d graph
    SPR = 200  # sec per runde

    # grid to run ball formula on
    M1, M2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

    def __init__(self, pos, system, gridpos, title, axislabels, limits):
        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos, projection="3d")
        super().__init__(pos, self.plot, title, axislabels, limits)

        # spesefik til 3d graf
        self.plot.set_zlim((limits[2][0], limits[2][1]))
        self.plot.set_zlabel(axislabels[2])

        self.spheres = []
        for o in self.system.objects:
            self.spheres.append(self.init_sphere(o))

        self.plot_graph()

    def plot_graph(self):

        kinetic_friction_coefficient = np.linspace(
            min_friction, max_friction, 100)
        starting_velocity = np.linspace(min_speed, max_speed, 100)

        X, Y = np.meshgrid(kinetic_friction_coefficient, starting_velocity)
        distances = distance_travelled(X, Y)

        # distances = np.zeros_like(X)
        # it = np.nditer([X, Y, distances], flags=[
        #                'multi_index'], op_flags=['readwrite'])
        # for friction_constant, vel, dist in it:
        #     dist[...] = distance_travelled(friction_constant, vel)

        self.plot.plot_surface(X, Y, distances, cmap="viridis")

    def init_sphere(self, o):
        # parametric equation sphere
        size = 0.05
        x = o.mu + (size * (max_friction - min_friction)) * \
            np.cos(self.M1)*np.sin(self.M2)
        y = o.v + (size * (max_speed - min_speed)) * \
            np.sin(self.M1)*np.sin(self.M2)

        d = distance_travelled(o.mu, o.v)
        z = d + (size * (max_length - min_length)) * np.cos(self.M2)
        # add sphere to plot
        return self.plot.plot_wireframe(x, y, z,  rstride=1, cstride=1, color=o.color, linewidth=0.25, facecolor=o.color, antialiased=True)

    def update(self, i, o):
        # self.plot.collections.remove(self.spheres[i])
        # self.spheres[i] = self.init_sphere(o)

        angle = self.system.t[-1] * 360 / self.SPR
        self.plot.view_init(np.sin(angle/150) * 15 + 30, angle)

        # self.plot.legend(loc=1, prop={'size': 8})
        ret_ = [self.plot]
        return ret_


def create_plot(type, pos, system, gridpos, title, axislabels, limits):
    if type == "3D":
        return Plot3D(pos, system, gridpos, title, axislabels, limits)
    elif type == "line":
        return friction_animation(pos, system, gridpos, title, axislabels, limits)
    elif type == "static":
        return static(pos, system, gridpos, title, axislabels, limits)


class static(Plot):

    def __init__(self, pos, system, gridpos, title, axislabels, limits):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)
        # Define the range of applied forces
        Fapp = range(0, 20)

        # Define the value of the static friction
        Fstatic = 8

        # Define the value of the kinetic friction
        Fkinetic = 4

        # Define the range of frictional forces
        Ffric = []
        for f in Fapp:
            if f <= Fstatic:
                Ffric.append(f)
            else:
                Ffric.append(Fkinetic)

        # Plot the graph
        self.plot.plot(Fapp, Ffric)

        # Mark the static friction and kinetic friction
        self.plot.axhline(y=Fstatic, color='r',
                          linestyle='--', label='Static Friction')
        self.plot.axhline(y=Fkinetic, color='g',
                          linestyle='--', label='Kinetic Friction')

        # Show the legend
        self.plot.legend()


class System:

    def __init__(self, objects, dt, save, saveAs=r"./animation.gif"):
        self.objects = objects
        self.dt = dt
        self.save = save
        self.saveAs = saveAs

        self.fig = plt.figure(figsize=(13, 9))
        self.plots = []
        self.t = [0]  # time

        plt.subplots_adjust(hspace=0.648, top=0.943, bottom=0.08)
        plt.style.use("dark_background")
        self.fig.patch.set_facecolor("black")
        self.fig.tight_layout()

        grid = self.fig.add_gridspec(4, 4)

        self.plots.append(create_plot(
            "static",
            1,
            self,
            grid[0:3, 0:2],
            "Applied Force vs. Frictional Force",
            ["Applied Force (N)",
             "Frictional Force (N)"],
            [[0, 18], [
                0, 9]]
        ))

        # type fig, gridpos, title, axislabels, limits
        self.plots.append(create_plot(
            "3D",
            2,
            self,
            grid[0:3, 2:4],
            "3D representation",
            ["kinetic coefficient of friction (mu)",
             "initial speed (m/s)", "length before stop"],
            [[min_friction, max_friction], [
                min_speed, max_speed], [min_length, max_length]]
        ))

        self.plots.append(create_plot(
            "line",
            3,
            self,
            grid[3, 0:4],
            "Visualization",
            ["Position (m)", ""],
            [[0, 5], [-0.2, 0.3]]
        ))

    def update_objects(self):
        ret_ = []
        for object in self.objects:
            ret_ += object.update(self.dt)
        return ret_

    def update_plots(self):
        ret_ = []
        for i, plot in enumerate(self.plots):
            for j, object in enumerate(self.objects):
                if type(plot) == Plot3D:
                    ret_ += plot.update(j, object)
                elif type(plot) == friction_animation:
                    ret_ += plot.update(self.t, object.vel_data)
        return ret_

    def animate(self, framenum):
        print(framenum)
        iterperframe = 1
        for i in range(iterperframe):
            self.t.append(framenum * self.dt)
            ret_ = []
            ret_ += self.update_objects()
            ret_ += self.update_plots()
        return ret_

    def run(self):
        # kjører animasjon i matplotlib
        self.animation = animation.FuncAnimation(
            self.fig,
            self.animate,
            fargs=(),
            interval=1,
            save_count=30,
            frames=550,
        )

        if self.save:
            self.save_as_gif()
        plt.show()

    def save_as_gif(self):
        # saves animation as gif using ffmpeg and outputs to specified location
        writer = animation.FFMpegWriter(fps=60, bitrate=18_000)
        self.animation.save(self.saveAs, writer=writer)


def distance_travelled(friction_constant, starting_velocity):
    g = 9.81   # acceleration due to gravity in m/s^2
    distance = starting_velocity**2 / (2 * friction_constant * g)

    return distance


def generate_colors(num_colors):
    """
    Generate a specified number of visually distinct colors as hexadecimal codes.
    """
    # Generate a 2D NumPy array of random HSV values
    hsv = np.random.rand(num_colors, 3)
    # Set the saturation and value/brightness values to ensure visual distinctness
    hsv[:, 1] = np.random.uniform(0.4, 1.0, size=num_colors)
    hsv[:, 2] = np.random.uniform(0.4, 1.0, size=num_colors)
    # Convert the HSV values to RGB values
    rgb = np.apply_along_axis(lambda x: colorsys.hsv_to_rgb(*x), 1, hsv)
    # Convert the RGB values to a hexadecimal code and add it to the list of colors
    hex_codes = ['#{:02x}{:02x}{:02x}'.format(
        int(r * 255), int(g * 255), int(b * 255)) for r, g, b in rgb]
    return hex_codes


if __name__ == "__main__":
    max_friction = 0.02
    min_friction = 0.0046
    max_speed = 2.7  # 10 km/h
    min_speed = 1
    max_length = distance_travelled(min_friction, max_speed)
    min_length = distance_travelled(max_friction, min_speed)

    count = 3
    colors = generate_colors(count)
    objects = []
    for color in colors:
        objects.append(Object("skøyte",  # name
                              color,  # color green
                              (0.3, 0.2),  # box size
                              0,  # position
                              # initial velocity
                              np.random.uniform(min_speed, max_speed),
                              0.0046  # coefficient of friction https://www.sciencedirect.com/science/article/abs/pii/002192909290099M
                              ))

    # objects, dt, save
    system = System(objects, 0.1, True)
    system.run()
