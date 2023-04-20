from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


# particle class stores all information about the particle
class Object:
    def __init__(self, name, color, radius, p, v, q, m):
        global E
        # Initial values
        self.name = name
        self.color = color
        self.radius = radius
        self.q = q
        self.m = m
        self.F_e = q * E

        self.p = np.array(p)          # position
        self.v = np.array(v)          # velocity
        self.a = np.array([0, 0, 0])  # acceleration

        # arrays for saving state and graph
        self.pos_data = [[p[0]], [p[1]], [p[2]]]
        self.vel_data = [[v[0]], [v[1]], [v[2]]]
        self.acc_data = [[self.a[0]], [self.a[1]], [self.a[2]]]

    def update(self, dt):
        global B

        self.F_m = np.cross(self.q * self.v, B)   # magnetisk kraft, N
        sum_F = self.F_e + self.F_m               # kraftsum, N
        self.a = sum_F / self.m              # akselerasjon, m/s^2

        self.v = self.v + self.a * dt   # regner ut ny fart
        self.p = self.p + self.v * dt   # regner ut ny posisjon

        self.logstate()

    def logstate(self):
        # saves the current state for plotting
        for i in range(3):
            self.pos_data[i].append(self.p[i])
            self.vel_data[i].append(self.v[i])
            self.acc_data[i].append(self.a[i])


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


class Linegraph(Plot):

    def __init__(self, pos, system, gridpos, title, axislabels, limits, graphlabels=["x", "y", "z"]):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.plot.axhline(y=0, linewidth=0.7, color='w')

        self.graphs = []
        for label in graphlabels:
            self.graphs += self.plot.plot([], [], label=label)

    def reframe(self):
        # makes sure all the date being displayd is within the plot
        # x
        self.limits[0][0] = self.system.t[-1] - 5  # history 5 sec
        self.limits[0][1] = self.system.t[-1]

        # y
        if self.pos == 0:  # vel
            for o in self.system.objects:
                self.limits[1][0] = min(
                    min(self.limits[1][0], o.v[0]), min(o.v[1], o.v[2]))
                self.limits[1][1] = max(
                    max(self.limits[1][1], o.v[0]), max(o.v[1], o.v[2]))
        elif self.pos == 1:  # acc
            for o in self.system.objects:
                self.limits[1][0] = min(
                    min(self.limits[1][0], o.a[0]), min(o.a[1], o.a[2]))
                self.limits[1][1] = max(
                    max(self.limits[1][1], o.a[0]), max(o.a[1], o.a[2]))

        border = 1.1
        self.plot.set_xlim((self.limits[0][0], self.limits[0][1]))
        self.plot.set_ylim(
            (self.limits[1][0] * border, self.limits[1][1] * border))

    def update(self, xaxis, datasets):
        for i, data in enumerate(datasets):
            self.graphs[i].set_data(xaxis, data)

        self.plot.legend(loc=1, prop={'size': 8})

        self.reframe()

        ret_ = [self.plot]
        return ret_


class Plot3D(Plot):

    # rotation speed on 3d graph
    SPR = 300  # sec per runde

    # grid to run ball formula on
    M1, M2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

    def __init__(self, pos, system, gridpos, title, axislabels, limits):
        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos, projection="3d")
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.spheres = []
        self.trajectories = []
        self.vel_vectors = []
        self.acc_vectors = []

        # spesefik til 3d graf
        self.plot.set_zlim((limits[2][0], limits[2][1]))
        self.plot.set_zlabel(axislabels[2])

        self.sim_time_label = self.plot.text2D(
            0, 0.95, '', transform=self.plot.transAxes)

        for o in system.objects:
            # creates velocity and acceleration vectors, a sphere and trajectory for visualizing every object
            self.vel_vectors.append(self.plot.quiver( 0, 0, 0, 0, 0, 0, 
                                                        color="red", label="v"))
            self.acc_vectors.append(self.plot.quiver( 0, 0, 0, 0, 0, 0, 
                                                        color="blue", label="a"))
            self.spheres.append(self.init_sphere(o, o.radius, o.p))
            self.trajectories += self.plot.plot3D(o.pos_data[0],
                                                    o.pos_data[1],
                                                    o.pos_data[2],
                                                    linewidth=1,
                                                    color=o.color,
                                                    label=o.name
                                                    )

    def init_sphere(self, o, r, p=[0, 0, 0]):

        # parametric equation sphere
        x = p[0] + r * np.cos(self.M1)*np.sin(self.M2)
        y = p[1] + r * np.sin(self.M1)*np.sin(self.M2)
        z = p[2] + r * np.cos(self.M2)
        # add sphere to plot
        return self.plot.plot_wireframe(x, y, z,  rstride=1, cstride=1, color="b", linewidth=0.25, facecolor=o.color, antialiased=True)

    def reframe(self):
        # makes sure all the data being displayd is within the plot

        for i in range(3):
            for o in self.system.objects:
                self.limits[i][0] = min(self.limits[i][0], o.p[i])
                self.limits[i][1] = max(self.limits[i][1], o.p[i])

        border = 1.1
        self.plot.set_xlim((self.limits[0][0] * border, self.limits[0][1] * border))
        self.plot.set_ylim((self.limits[1][0] * border, self.limits[1][1] * border))
        self.plot.set_zlim((self.limits[2][0] * border, self.limits[2][1] * border))

    def update(self, i, o):
        self.plot.collections.remove(self.spheres[i])
        self.spheres[i] = self.init_sphere(o, o.radius, o.p)

        # plotter banen til objektet
        self.trajectories[i].set(
            data_3d=(o.pos_data[0], o.pos_data[1], o.pos_data[2]), color=o.color)

        # plotter fartsvector
        self.vel_vectors[i].set_segments( [[[o.p[0], o.p[1], o.p[2]],
                                            [o.p[0] + o.v[0], o.p[1] + o.v[1], o.p[2] + o.v[2]]]])
        # plotter akselerasjonsvektor
        self.acc_vectors[i].set_segments( [[[o.p[0], o.p[1], o.p[2]],
                                            [o.p[0] + o.a[0], o.p[1] + o.a[1], o.p[2] + o.a[2]]]])

        angle = self.system.t[-1] * 360 / self.SPR
        self.plot.view_init(np.sin(angle/150) * 15 + 30, angle)

        self.sim_time_label.set_text(
            "Simulation Time: " + str(np.round(self.system.t[-1], 2)))

        self.plot.legend(loc=1, prop={'size': 8})
        self.reframe()
        ret_ = [self.plot]
        return ret_


def create_plot(type, pos, system, gridpos, title, axislabels, limits):
    if type == "3D":
        return Plot3D(pos, system, gridpos, title, axislabels, limits)
    elif type == "line":
        return Linegraph(pos, system, gridpos, title, axislabels, limits)


class System:

    def __init__(self, objects, dt, save, saveAs=r"./animation.gif"):
        self.objects = objects
        self.dt = dt
        self.save = save
        self.saveAs = saveAs

        self.fig = plt.figure(figsize=(13, 8))
        self.plots = []
        self.t = [0]  # time

        plt.subplots_adjust(hspace=0.3)
        plt.style.use("dark_background")
        self.fig.patch.set_facecolor("black")
        self.fig.tight_layout()

        grid = self.fig.add_gridspec(2, 3)

        # type fig, gridpos, title, axislabels, limits
        self.plots.append(create_plot(
            "line",
            0,
            self,
            grid[0, 0:1],
            "Velocity Plot",
            ["Time: (s)", "Velocity (m/s)"],
            [[0, 5], [-0.5, 0.5]]
        ))
        self.plots.append(create_plot(
            "line",
            1,
            self,
            grid[1, 0:1],
            "Acceleration Plot",
            ["Time: (s)", "Acceleration (m/s^2)"],
            [[0, 5], [-0.05, 0.05]]
        ))
        self.plots.append(create_plot(
            "3D",
            2,
            self,
            grid[0:2, 1:3],
            "3D representation",
            ["X position (m)", "Y position (m)", "Z position (m)"],
            [[-0.5, 0.5], [-0.5, 0.5], [-0.5, 0.5]]
        ))

    def update_objects(self):
        for object in self.objects:
            object.update(self.dt)

    def update_plots(self):
        ret_ = []
        for i, plot in enumerate(self.plots):
            for j, object in enumerate(self.objects):
                if type(plot) == Plot3D:
                    ret_ += plot.update(j, object)
                elif type(plot) == Linegraph:
                    if i == 0:
                        ret_ += plot.update(self.t, object.vel_data)
                    elif i == 1:
                        ret_ += plot.update(self.t, object.acc_data)
        return ret_

    def animate(self, framenum):
        print(framenum)
        iterperframe = 1
        for i in range(iterperframe):
            self.t.append(framenum * self.dt)
            self.update_objects()
            ret_ = []
            ret_ += self.update_plots()

    def run(self):
        # kjører animasjon i matplotlib
        self.animation = animation.FuncAnimation(
            self.fig,
            self.animate,
            fargs=(),
            interval=1,
            save_count=20,
            frames=200,
        )

        if self.save:
            self.save_as_gif()
        plt.show()

    def save_as_gif(self):
        # saves animation as gif using ffmpeg and outputs to specified location
        writer = animation.FFMpegWriter(fps=60, bitrate=18_000)
        self.animation.save(self.saveAs, writer=writer)


if __name__ == "__main__":
    # Konstanter
    E = np.array([0, -0.0040, 0])  # elektrisk felt, N/C
    B = np.array([0, 0, -0.010])   # magnetisk felt, T


    # [x, y ,z]
    # name, color, radius, position, velocity, electric charge, mass
    particles = [Object("particle",  # name
                        "g",  # color green
                        0.05,  # radius
                        [0, 0, 0],  # position
                        [0.24, 0, 0],  # velocity
                        1.0,  # electric charge
                        0.010  # mass
                        )]

    # objects, dt, save
    system = System(particles, 0.1, False)
    system.run()
