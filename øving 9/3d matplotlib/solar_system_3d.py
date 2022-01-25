
import itertools
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from vectors import Vector

class SolarSystem:
    def __init__(self, size):
        self.size = size
        # self.projection_2d = projection_2d
        self.bodies = []

        # self.fig, self.ax = plt.subplots( 1, 1, subplot_kw={projection: "3d"}, figsize=(10, 8),)
        self.fig = plt.figure(figsize=(13, 8))
        self.fig.tight_layout()
        # self.ax = []
        self.m1, self.m2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

        # grid = fig.add_gridspec(2, 3)
        # self.ax.append(fig.add_subplot(projection="3d"))
        self.ax = self.fig.add_subplot(projection="3d")

        # if self.projection_2d:
            # self.ax.view_init(10, 0)
        # else:
            # self.ax.view_init(0, 0)

        # self.fig.tight_layout()
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))

    def add_body(self, body):
        self.bodies.append(body)

    # def draw_all(self):
        # self.ax.set_xlim((-self.size / 2, self.size / 2))
        # self.ax.set_ylim((-self.size / 2, self.size / 2))
        # self.ax.set_zlim((-self.size / 2, self.size / 2))
        # if self.projection_2d:
        #     self.ax.xaxis.set_ticklabels([])
        #     self.ax.yaxis.set_ticklabels([])
        #     self.ax.zaxis.set_ticklabels([])
        # else:
        #     self.ax.axis(False)

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)

    def save(self):
        # set output file
        f = r"./animation.gif"
        writer = animation.FFMpegWriter(fps=60, bitrate=18000)
        self.ani.save(f)

    def update(self, framenum):
        # return [] + self.bodies
        self.bodies.sort(key=lambda item: item.position[0])
        # foo = np.ndarray()
        foo = []
        for body in self.bodies:
            body.move()
            # print("-------------------------")
            # print(*body.position)
            # body.plot.set(offsets=body.position)
            # body.plot.set(offsets=body.position,color="r")

            # if (body.sphere):
                # self.ax.collections.remove(body.sphere)

            # parameter fremsitilling av en kule
            # print(body.position)
            # x = body.position[0] + body.radius * np.cos(self.m1)*np.sin(self.m2)
            # y = body.position[1] + body.radius * np.sin(self.m1)*np.sin(self.m2)
            # z = body.position[2] + body.radius * np.cos(self.m2)
            # body.sphere = self.ax.plot_wireframe( x, y, z,  rstride=1, cstride=1, color='b', linewidth=0.25)
            # body.sphere.set(offsets=body.position)
            body.sphere.set(offsets=[1e10, 0, 0])
            foo.append(body.sphere)
        print(foo)

        return foo

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, fargs=(), interval=1, save_count=50,frames=50, blit=True)
        plt.show()


class SolarSystemBody:
    min_display_size = 10
    display_log_base = 1.3

    def __init__(
        self,
        solar_system,
        mass,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10
    ):
        self.solar_system = solar_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(velocity)
        self.display_size = max( math.log(self.mass, self.display_log_base), self.min_display_size,)
        self.colour = "black"
        self.radius = radius

        self.m1, self.m2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = self.radius * np.cos(self.m1)*np.sin(self.m2)
        y = self.radius * np.sin(self.m1)*np.sin(self.m2)
        z = self.radius * np.cos(self.m2)
        self.sphere = self.solar_system.ax.plot_wireframe( x, y, z, rstride=1, cstride=1, color='b', linewidth=0.25)

        self.solar_system.add_body(self)


        # self.plot = self.solar_system.ax.scatter( *self.position, marker="o", linewidth=self.display_size + self.position[0] / 30, color=self.colour)
        # self.plot = self.solar_system.ax.scatter( *self.position, marker="o", linewidth=1000, color=self.colour)
        # self.plot.set_animated(true)
        # print(self.plot)

    def move(self):
        # self.position = tuple(np.add(self.position, self.velocity))
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2],
        )

    # def draw(self):
        # self.solar_system.ax.plot( *self.position, marker="o", markersize=self.display_size + self.position[0] / 30, color=self.colour)
        # if self.solar_system.projection_2d:
        #     self.solar_system.ax.plot(
        #         self.position[0],
        #         self.position[1],
        #         -self.solar_system.size / 2,
        #         marker="o",
        #         markersize=self.display_size / 2,
        #         color=(.5, .5, .5),
        #     )

    def accelerate_due_to_gravity(self, other):
        distance = Vector(other.position) - Vector(self.position)
        # print(repr(distance))
        distance_mag = distance.get_magnitude()

        force_mag = self.mass * other.mass / (distance_mag ** 2)
        force = distance.normalize() * force_mag

        reverse = 1
        for body in self, other:
            acceleration = force / body.mass
            body.velocity += acceleration * reverse
            reverse = -1



class Sun(SolarSystemBody):
    def __init__(
        self,
        solar_system,
        mass=10_000,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10
    ):
        super(Sun, self).__init__(solar_system, mass, position, velocity, radius)
        self.colour = "yellow"

class Planet(SolarSystemBody):
    colours = itertools.cycle([(1, 0, 0), (0, 1, 0), (0, 0, 1)])

    def __init__(
        self,
        solar_system,
        mass=10,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        radius=1e10
    ):
        super(Planet, self).__init__(solar_system, mass, position, velocity, radius)
        self.colour = next(Planet.colours)

# class simulation(SolarSystem):
    
    # def __init__(SolarSystem,):

        # fig, ax = plt.subplots(1, 1, figsize=(10, 8))

        # title = ax.text(0.16, 0.97, f"Number of Iterations = {m}", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, transform=ax.transAxes, ha="center")




# while True:
    # solar_system.calculate_all_body_interactions()
    # solar_system.update_all()
    # solar_system.draw_all()