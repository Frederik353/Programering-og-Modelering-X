
import itertools
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from vectors import Vector


class SolarSystem:
    def __init__(self, size, save=False):
        self.size = size
        self.bodies = []
        self.save_gif = save

        self.fig = plt.figure(figsize=(13, 8))
        plt.style.use('dark_background')
        self.fig.patch.set_facecolor("black")
        plt.rcParams['grid.color'] = (1, 1, 1, 0.1)
        self.fig.tight_layout()
        self.ax = []
        grid = self.fig.add_gridspec(2, 3)
        self.ax.append(self.fig.add_subplot(grid[0, 0:1], projection="3d"))
        self.ax.append(self.fig.add_subplot(grid[1:, 0:1], projection="3d"))
        self.ax.append(self.fig.add_subplot(grid[0:2, 1:3], projection="3d"))
        self.sim_time_label = self.ax[2].text2D(
            0, 0.95, '', transform=self.ax[2].transAxes)

        self.m1, self.m2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

        border = 5e8 / 2
        self.init_plots(0, -border, border, -border, border, -border, border, "Distance: (m)", "Distance: (m)",
                        "Distance: (m)", "title", (0, 0, 0), 45, 45)  # limits fixed later
        border = 12e12 / 2
        self.init_plots(1, -border, border, -border, border, -border, border,
                        "Distance: (m)", "Distance: (m)", "Distance: (m)", "title", (0, 0, 0), 45, 45)
        border = 5e11 / 2
        self.init_plots(2, -border, border, -border, border, -border, border,
                        "Distance: (m)", "Distance: (m)", "Distance: (m)", "title", (0, 0, 0), 45, 45)

    def init_plots(self, plot, xmin, xmax, ymin, ymax, zmin, zmax, xlabel, ylabel, zlabel, title, bgcolor, elevation, azimuth):
        self.ax[plot].set_xlim((xmin, xmax))
        self.ax[plot].set_ylim((ymin, ymax))
        self.ax[plot].set_zlim((zmin, zmax))
        self.ax[plot].set_xlabel(xlabel)
        self.ax[plot].set_ylabel(ylabel)
        self.ax[plot].set_zlabel(zlabel)
        self.ax[plot].w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        self.ax[plot].w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        self.ax[plot].w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0))
        # ax[plotx, ploty].grid()
        # ax[plotx,ploty].legend()
        self.ax[plot].set_title(title)
        self.ax[plot].view_init(elevation, azimuth)

    def add_body(self, body):
        self.bodies.append(body)

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)

    def run(self):
        self.ax[2].legend()
        self.ani = animation.FuncAnimation(self.fig, self.update, fargs=(
        ), interval=1, save_count=1_00, frames=10_00, blit=False)

        if (self.save_gif):
            self.save()
        plt.show()

    def save(self):
        # set output file
        f = r"./animation.gif"
        writer = animation.FFMpegWriter(fps=60, bitrate=18_000)
        self.ani.save(f)

    def update(self, framenum):

        # self.bodies.sort(key=lambda item: item.position[0])

        self.sim_time_label.set_text(f"Day: {framenum}")
        print(framenum)

        foo = []
        self.calculate_all_body_interactions()
        for int, body in enumerate(self.bodies):
            body.move()

            for plot, axis in enumerate(self.ax):
                if (plot == 0):
                    continue

                body.posarr[plot][0].append(body.position[0])
                body.posarr[plot][1].append(body.position[1])
                body.posarr[plot][2].append(body.position[2])

                # print(axis.collections, body.sphere[plot])
                axis.collections.remove(body.sphere[plot])

                radiusfactor = [1e7, 2e11, 1.2e10]
                # parameter fremsitilling av en kule
                x = body.position[0] + (body.radius +
                                        radiusfactor[plot]) * np.cos(self.m1)*np.sin(self.m2)
                y = body.position[1] + (body.radius +
                                        radiusfactor[plot]) * np.sin(self.m1)*np.sin(self.m2)
                z = body.position[2] + (body.radius +
                                        radiusfactor[plot]) * np.cos(self.m2)
                body.sphere[plot] = axis.plot_wireframe(
                    x, y, z,  rstride=1, cstride=1, color='b', linewidth=0.25, facecolor=body.color, antialiased=True)

                body.trace[plot][0].set(
                    data_3d=(body.posarr[plot][0], body.posarr[plot][1], body.posarr[plot][2]), color=body.color)

                axis.texts.remove(body.text[plot])

                foo = 7e11

                body.text[plot] = axis.text(
                    *np.add(body.position, foo * 1e-1), body.name)

                if (body.name == "Earth" and plot == 0):
                    axis.set_xlim(
                        (body.position[0] - foo, body.position[0] + foo))
                    axis.set_ylim(
                        (body.position[1] - foo, body.position[1] + foo))
                    axis.set_zlim(
                        (body.position[2] - foo, body.position[2] + foo))

            # for index in [4,5]:
            if (body.name == "Earth" or body.name == "Moon"):
                plot = 0

                self.ax[plot].collections.remove(body.sphere[plot])

                radiusfactor = [2e7]

                if (body.name == "Earth"):
                    position = [0, 0, 0]
                else:
                    position = [
                        body.position[0] - self.bodies[3].position[0],
                        body.position[1] - self.bodies[3].position[1],
                        body.position[2] - self.bodies[3].position[2],
                    ]

                body.posarr[plot][0].append(position[0])
                body.posarr[plot][1].append(position[1])
                body.posarr[plot][2].append(position[2])

                # parameter fremsitilling av en kule
                x = position[0] + (body.radius + radiusfactor[plot]
                                   ) * np.cos(self.m1)*np.sin(self.m2)
                y = position[1] + (body.radius + radiusfactor[plot]
                                   ) * np.sin(self.m1)*np.sin(self.m2)
                z = position[2] + (body.radius +
                                   radiusfactor[plot]) * np.cos(self.m2)
                body.sphere[plot] = self.ax[plot].plot_wireframe(
                    x, y, z,  rstride=1, cstride=1, color='b', linewidth=0.25, facecolor=body.color, antialiased=True)

                body.trace[plot][0].set(
                    data_3d=(body.posarr[plot][0], body.posarr[plot][1], body.posarr[plot][2]), color=body.color)

                self.ax[plot].texts.remove(body.text[plot])
                foo = 1e8
                body.text[plot] = self.ax[plot].text(
                    *np.add(position, foo), body.name)

        return self.ax


class SolarSystemBody:
    min_display_size = 10
    display_log_base = 1.3

    def __init__(
        self,
        solar_system,
        mass=1e20,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10,
        color="magenta",
        name="Unknown"
    ):
        self.solar_system = solar_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(velocity)
        self.display_size = max(
            math.log(self.mass, self.display_log_base), self.min_display_size,)
        self.color = color
        self.name = name
        self.radius = radius

        self.m1, self.m2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.radius * np.cos(self.m1)*np.sin(self.m2)
        y = self.radius * np.sin(self.m1)*np.sin(self.m2)
        z = self.radius * np.cos(self.m2)

        self.sphere = []
        self.trace = []
        self.text = []
        foo = 2 * 1e8
        for plot, axis in enumerate(self.solar_system.ax):
            self.trace.append(axis.plot3D(
                [], [], [], linewidth=1, color=self.color, label=self.name))
            if (plot == 0 and not (self.name == "Earth" or self.name == "Moon")):
                self.sphere.append("empty")
                # self.trace.append("empty")
                self.text.append("empty")
                continue

            self.sphere.append(axis.plot_wireframe(
                x, y, z, rstride=1, cstride=1, color=self.color, linewidth=0.25, label=self.name))
            self.text.append(
                axis.text(*np.add(self.position, foo * 1e-2), self.name))

        self.posarr = [[[], [], []], [[], [], []], [[], [], []]]

        self.solar_system.add_body(self)

    def move(self):
        foo = 8.64e4
        self.position = (
            self.position[0] + self.velocity[0] * foo,
            self.position[1] + self.velocity[1] * foo,
            self.position[2] + self.velocity[2] * foo,
        )

    def accelerate_due_to_gravity(self, other):

        distance = Vector(other.position) - Vector(self.position)
        distance_mag = distance.get_magnitude()

        G = 6.67408e-11  # m**3 kg**-1 s**-2
        force_mag = G * (self.mass * other.mass / (distance_mag ** 2))
        force = distance.normalize() * force_mag

        reverse = 1
        for body in self, other:
            acceleration = (force / body.mass)
            body.velocity += acceleration * (reverse * 8.64e4)
            reverse = -1


class Sun(SolarSystemBody):
    def __init__(
        self,
        solar_system,
        mass,
        position,
        velocity,
        radius, color, name
    ):
        super(Sun, self).__init__(solar_system, mass,
                                  position, velocity, radius, color, name)


class Planet(SolarSystemBody):
    def __init__(
        self,
        solar_system,
        mass=10,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10,
        color="magenta",
        name="Unknown"
    ):
        super(Planet, self).__init__(solar_system, mass,
                                     position, velocity, radius, color, name)


if __name__ == "__main__":
    import config
    config.main()
