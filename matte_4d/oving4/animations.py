import colorsys
import copy

import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

# particle class stores all information about the particle


class Object:

    def __init__(self, name, color, size, p, v0, mu):
        # Initial values
        self.name = name
        self.color = color
        self.size = size

        self.p = p  # position


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

        self.plot.grid(True, color='darkgrey', linestyle='--', linewidth=0.25)


class Newton_plot(Plot):

    # annotations = []

    def __init__(self, pos, system, gridpos, title, axislabels, limits):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.plot.axhline(y=0, linewidth=0.7, color='w')

        self.tangents = []
        self.annotations = []
        self.limits = limits
        self.graph = False
        self.step = 0
        self.limits_prev = limits
        self.smoothness = 50
        self.border = 0

        # self.height_factor = 1 + 2 * self.border
        # self.height_factor = 0.5
        # self.width_factor = 0.005
        # self.h = (self.limits[1][1] - self.limits[1][0]) * self.height_factor
        # self.w = (self.limits[1][1] - self.limits[1][0]) * self.width_factor
        # self.prev_w = self.w

        # self.markers.append( plt.Rectangle((limits[0][0], -self.h / 2), width=self.w, height=self.h, fc="#007777"))
        # self.markers.append( plt.Rectangle((limits[0][1], -self.h / 2), width=self.w, height=self.h, fc="#007777"))

        # self.plot.add_patch(self.markers[0])
        # self.plot.add_patch(self.markers[1])

        self.err = (self.limits[1][1] - self.limits[1][0]) / 2
        self.current_estimate = 0.5
        self.prev_estimate = 0.5

        self.left_estimate = self.limits[0][0]
        self.right_estimate = self.limits[0][1]

    # def f(self, x):
    #     return ((2 - 2 * 3**x) * x**2 + 4 * (2 * x - 2) * 3**x + 4 *
    #             (2 - 2 * x))

    # def df(self, x):
    #     return -2 * (x - 2) * (2 * 3**x + 3**x * x * np.log(3) - 3**x * np.log(9) - 2)

    def f(self, x):
        return -x + np.cos(x)

    def df(self, x):
        return -1 - np.sin(x)

    def update(self, dt):
        # step = (self.step % self.smoothness)
        step = (self.step % self.smoothness
                ) if self.step % self.smoothness != 0 else self.smoothness

        # left x
        lx_step_size = (self.limits[0][0] -
                        self.limits_prev[0][0]) / self.smoothness
        lx_start = self.limits_prev[0][0]
        lx = lx_start + step * lx_step_size

        # right x
        rx_step_size = (self.limits_prev[0][1] -
                        self.limits[0][1]) / self.smoothness
        rx_start = self.limits_prev[0][1]
        rx = rx_start - step * rx_step_size

        # bottom y
        by_step_size = (self.limits[1][0] -
                        self.limits_prev[1][0]) / self.smoothness
        by_start = self.limits_prev[1][0]
        by = by_start + step * by_step_size

        # top y
        ty_step_size = (self.limits_prev[1][1] -
                        self.limits[1][1]) / self.smoothness
        ty_start = self.limits_prev[1][1]
        ty = ty_start - step * ty_step_size

        border_x = (rx - lx) * self.border
        border_y = (ty - by) * self.border

        self.plot.set_xlim((lx - border_x, rx + border_x))
        self.plot.set_ylim((by - border_y, ty + border_y))

        # self.plot.legend(loc=1, prop={'size': 8})

        # annotations
        for ann in self.annotations:
            ann.remove()

        self.annotations.clear()

        frame_size_x = (rx + border_x) - (lx - border_x)
        frame_size_y = (ty + border_y) - (by - border_y)

        self.annotations.append(
            self.plot.annotate(
                f"Current estimate: {self.current_estimate}",
                xy=(0.008, 0.9),
                xycoords='axes fraction',  # Use axes coordinate system
                fontsize=12,
                bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.8)))

        self.annotations.append(
            self.plot.annotate(f"Max Error: {self.err}",
                               xy=(0.008, 0.8),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        self.annotations.append(
            self.plot.annotate(f"Iteration: {self.step // self.smoothness}",
                               xy=(0.008, 0.7),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        if self.step % self.smoothness == 0:

            self.limits_prev = copy.deepcopy(self.limits)
            x = self.current_estimate
            y = self.f(x)
            dy = self.df(x)

            # Determine the next estimate
            # if dy <= 0:
            #     self.left_estimate = self.current_estimate
            # else:
            #     self.right_estimate = self.current_estimate

            self.prev_estimate = self.current_estimate
            self.current_estimate = x - y / dy

            # error
            self.err = abs(self.current_estimate - self.prev_estimate)

            # step_size = abs(self.current_estimate - self.prev_estimate)
            # buffer_factor = 1

            x_min = min(self.current_estimate - self.err, self.prev_estimate)
            x_max = max(self.current_estimate + self.err, self.prev_estimate)

            x_range = np.linspace(self.limits[0][0] - border_x,
                                  self.limits[0][1] + border_x, 400)

            # Set X limits for the frame
            self.limits[0][0] = x_min
            self.limits[0][1] = x_max

            tangent_line = y + dy * (x_range - x)

            self.tangents.append(
                self.plot.plot(
                    x_range,
                    tangent_line,
                    color="orange",
                    markersize=5,
                ))

            self.plot.plot(self.current_estimate,
                           0,
                           marker='o',
                           markersize=10,
                           color='red')
            self.plot.plot(self.current_estimate,
                           self.f(self.current_estimate),
                           marker='o',
                           markersize=10,
                           color='green')
            self.plot.plot((self.current_estimate, self.current_estimate),
                           (0, self.f(self.current_estimate)),
                           linestyle='--')

            y = self.f(x_range)

            if self.graph:
                self.graph.remove()

            self.graph, = self.plot.plot(x_range,
                                         y,
                                         label='f(x)',
                                         color="aqua")
            mask = (x_range >= self.limits[0][0]) & (x_range
                                                     <= self.limits[0][1])
            y_in_range = y[mask]

            # fixed = max(abs(np.min(y_in_range)), np.max(y_in_range))  # fixes 0 to be in the middle of y axis
            fixed = abs(self.f(self.prev_estimate))
            self.limits[1][0] = -fixed
            self.limits[1][1] = fixed
            # self.limits[1][0] = np.min(y_in_range)
            # self.limits[1][1] = np.max(y_in_range)

        self.step += 1
        ret_ = [self.plot]
        return ret_


class Bisection_plot(Plot):

    # annotations = []

    def __init__(self, pos, system, gridpos, title, axislabels, limits):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.plot.axhline(y=0, linewidth=0.7, color='w')

        self.markers = []
        self.annotations = []
        self.limits = limits
        self.graph = False
        self.step = 0
        self.limits_prev = limits
        self.smoothness = 100
        self.border = 0.5

        # self.height_factor = 1 + 2 * self.border
        self.height_factor = 0.5
        self.width_factor = 0.005
        self.h = (self.limits[1][1] - self.limits[1][0]) * self.height_factor
        self.w = (self.limits[1][1] - self.limits[1][0]) * self.width_factor
        self.prev_w = self.w

        self.markers.append(
            plt.Rectangle((limits[0][0], -self.h / 2),
                          width=self.w,
                          height=self.h,
                          fc="#007777"))
        self.markers.append(
            plt.Rectangle((limits[0][1], -self.h / 2),
                          width=self.w,
                          height=self.h,
                          fc="#007777"))

        self.plot.add_patch(self.markers[0])
        self.plot.add_patch(self.markers[1])

        self.err = (self.limits[1][1] - self.limits[1][0]) / 2
        self.current_estimate = (self.limits[1][1] + self.limits[1][0]) / 2

    def f(self, x):
        return ((2 - 2 * 3**x) * x**2 + 4 * (2 * x - 2) * 3**x + 4 *
                (2 - 2 * x))

    def update(self, dt):
        # step = (self.step % self.smoothness)
        step = (self.step % self.smoothness
                ) if self.step % self.smoothness != 0 else self.smoothness

        # left x
        lx_step_size = (self.limits[0][0] -
                        self.limits_prev[0][0]) / self.smoothness
        lx_start = self.limits_prev[0][0]
        lx = lx_start + step * lx_step_size

        # right x
        rx_step_size = (self.limits_prev[0][1] -
                        self.limits[0][1]) / self.smoothness
        rx_start = self.limits_prev[0][1]
        rx = rx_start - step * rx_step_size

        # bottom y
        by_step_size = (self.limits[1][0] -
                        self.limits_prev[1][0]) / self.smoothness
        by_start = self.limits_prev[1][0]
        by = by_start + step * by_step_size

        # top y
        ty_step_size = (self.limits_prev[1][1] -
                        self.limits[1][1]) / self.smoothness
        ty_start = self.limits_prev[1][1]
        ty = ty_start - step * ty_step_size

        # border = (self.limits[0][1] - self.limits[0][0]) * self.border
        border_x = (rx - lx) * self.border
        border_y = (ty - by) * self.border

        self.plot.set_xlim((lx - border_x, rx + border_x))
        self.plot.set_ylim((by - border_y, ty + border_y))

        # self.plot.legend(loc=1, prop={'size': 8})

        self.prev_w = self.w
        self.w = (rx - lx) * self.width_factor

        self.h = (ty - by) * self.height_factor

        for marker in self.markers:
            marker.set_height(self.h)
            x, _ = marker.get_xy()
            marker.set_width(self.w)
            marker.set_xy((x - (self.w - self.prev_w) / 2, -self.h / 2))

        # annotations
        for ann in self.annotations:
            ann.remove()
        self.annotations.clear()

        self.annotations.append(
            self.plot.annotate(f"Current estimate: {self.current_estimate}",
                               xy=(0.008, 0.9),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))
        self.annotations.append(
            self.plot.annotate(f"Max Error: {self.err}",
                               xy=(0.008, 0.8),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        self.annotations.append(
            self.plot.annotate(f"Iteration: {self.step // self.smoothness}",
                               xy=(0.008, 0.7),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        if self.step % self.smoothness == 0:
            a = self.limits[0][0]
            b = self.limits[0][1]

            self.limits_prev = copy.deepcopy(self.limits)

            x = np.linspace(a - border_x, b + border_x, 400)
            y = self.f(x)

            if self.graph:
                self.graph.remove()

            self.graph, = self.plot.plot(x, y, label='f(x)', color="aqua")

            if self.f(a) * self.f(b) >= 0:
                raise ValueError(
                    "The function must have different signs at endpoints a and b."
                )

            mid_x = (a + b) / 2
            mid_y = self.f(mid_x)
            self.current_estimate = mid_x

            self.plot.plot(mid_x,
                           mid_y,
                           marker='o',
                           markersize=10,
                           color='red')

            if self.f(a) * mid_y < 0:
                b = mid_x
            else:
                a = mid_x

            self.markers.append(
                plt.Rectangle((mid_x - self.w / 2, -self.h / 2),
                              width=self.w,
                              height=self.h,
                              fc=generate_colors(1)[0]))

            self.plot.add_patch(self.markers[-1])

            # error
            self.err = (b - a)

            self.limits[0][0] = a
            self.limits[0][1] = b

            mask = (x >= a) & (x <= b)
            y_in_range = y[mask]

            fixed = max(
                abs(np.min(y_in_range)),
                np.max(y_in_range))  # fixes 0 to be in the middle of y axis
            self.limits[1][0] = -fixed
            self.limits[1][1] = fixed
            # self.limits[1][0] = np.min(y_in_range)
            # self.limits[1][1] = np.max(y_in_range)

        self.step += 1
        ret_ = [self.plot]
        return ret_


class Fixed_point_plot(Plot):

    # annotations = []

    def __init__(self, pos, system, gridpos, title, axislabels, limits, g):

        self.system = system
        self.plot = self.system.fig.add_subplot(gridpos)
        super().__init__(pos, self.plot, title, axislabels, limits)

        self.plot.axhline(y=0, linewidth=0.7, color='w')

        self.annotations = []
        self.limits = limits
        self.graphs = []
        self.step = 0
        self.limits_prev = limits
        self.smoothness = 50
        self.border = 0.05

        self.g = g

        self.err = (self.limits[1][1] - self.limits[1][0]) / 2
        self.current_estimate = 4
        self.prev_estimate = 0.5

    def f(self, x):
        return (x - 3) * (x + 1)

    def update(self, dt):
        step = (self.step % self.smoothness
                ) if self.step % self.smoothness != 0 else self.smoothness

        # left x
        lx_step_size = (self.limits[0][0] -
                        self.limits_prev[0][0]) / self.smoothness
        lx_start = self.limits_prev[0][0]
        lx = lx_start + step * lx_step_size

        # right x
        rx_step_size = (self.limits_prev[0][1] -
                        self.limits[0][1]) / self.smoothness
        rx_start = self.limits_prev[0][1]
        rx = rx_start - step * rx_step_size

        # bottom y
        by_step_size = (self.limits[1][0] -
                        self.limits_prev[1][0]) / self.smoothness
        by_start = self.limits_prev[1][0]
        by = by_start + step * by_step_size

        # top y
        ty_step_size = (self.limits_prev[1][1] -
                        self.limits[1][1]) / self.smoothness
        ty_start = self.limits_prev[1][1]
        ty = ty_start - step * ty_step_size

        border_x = (rx - lx) * self.border
        border_y = (ty - by) * self.border

        self.plot.set_xlim((lx - border_x, rx + border_x))
        self.plot.set_ylim((by - border_y, ty + border_y))

        # self.plot.legend(loc=1, prop={'size': 8})

        # annotations
        for ann in self.annotations:
            ann.remove()

        self.annotations.clear()

        frame_size_x = (rx + border_x) - (lx - border_x)
        frame_size_y = (ty + border_y) - (by - border_y)

        self.annotations.append(
            self.plot.annotate(
                f"Current estimate: {self.current_estimate}",
                xy=(0.008, 0.9),
                xycoords='axes fraction',  # Use axes coordinate system
                fontsize=12,
                bbox=dict(boxstyle='round,pad=0.5', fc='black', alpha=0.8)))

        self.annotations.append(
            self.plot.annotate(f"Max Error: {self.err}",
                               xy=(0.008, 0.8),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        self.annotations.append(
            self.plot.annotate(f"Iteration: {self.step // self.smoothness}",
                               xy=(0.008, 0.7),
                               xycoords='axes fraction',
                               fontsize=12,
                               bbox=dict(boxstyle='round,pad=0.5',
                                         fc='black',
                                         alpha=0.8)))

        if self.step % self.smoothness == 0:
            self.limits_prev = copy.deepcopy(self.limits)
            # x = self.current_estimate
            # y = self.f(x)

            self.limits[0][1] = max(self.prev_estimate,
                                    self.current_estimate) + border_x
            self.limits[0][0] = min(self.prev_estimate,
                                    self.current_estimate) - border_x

            x_range = np.linspace(
                min(self.limits[0][0], self.limits_prev[0][0]) - border_x,
                max(self.limits[0][1], self.limits_prev[0][1]) + border_x, 400)
            self.prev_estimate = self.current_estimate
            self.current_estimate = self.g(self.current_estimate)

            # Set X limits for the frame

            # error
            self.err = abs(self.current_estimate - self.prev_estimate)

            self.plot.plot(self.current_estimate,
                           0,
                           marker='o',
                           markersize=10,
                           color='red')

            self.plot.plot(self.current_estimate,
                           self.f(self.current_estimate),
                           marker='o',
                           markersize=10,
                           color='green')

            self.plot.plot(
                (self.current_estimate, self.current_estimate),
                (self.g(self.current_estimate), self.current_estimate),
                linestyle='--',
                color="red")

            self.plot.plot((self.prev_estimate, self.current_estimate),
                           (self.current_estimate, self.current_estimate),
                           linestyle='--',
                           color="red")

            self.plot.plot((self.prev_estimate, self.prev_estimate),
                           (self.prev_estimate, self.g(self.prev_estimate)),
                           linestyle='--',
                           color="red")

            fy = self.f(x_range)
            gy = self.g(x_range)

            for graph in self.graphs:
                graph.remove()

            self.graphs.clear()

            self.graphs += self.plot.plot(x_range,
                                          fy,
                                          label='f(x)',
                                          color="aqua")
            self.graphs += self.plot.plot(x_range,
                                          gy,
                                          label='g(x)',
                                          color="orange")
            self.graphs += self.plot.plot(x_range,
                                          x_range,
                                          label='g(x)',
                                          color="purple")

            mask = (x_range >= self.limits[0][0]) & (x_range
                                                     <= self.limits[0][1])

            y_in_range = fy[mask]

            # fixed = max(abs(np.min(y_in_range)), np.max(y_in_range))  # fixes 0 to be in the middle of y axis
            # fixed = max(abs(self.g(self.prev_estimate)), abs(self.g(self.current_estimate)))

            fixed = max(abs(self.prev_estimate), abs(self.current_estimate))

            self.limits[1][1] = fixed  # g1
            self.limits[1][0] = fixed - abs(
                self.prev_estimate - self.current_estimate)  # plot g1

            self.limits[1][0] = -fixed  # plot g3
            self.limits[1][1] = -fixed + abs(
                self.current_estimate - self.g(self.current_estimate)) * 10

            # self.limits[1][0] = fixed * 0.1  # g2
            # self.limits[1][1] = fixed  # g2

            # self.limits[1][0] = np.min(y_in_range)
            # self.limits[1][1] = np.max(y_in_range)

        self.step += 1
        ret_ = [self.plot]
        return ret_


def create_plot(type,
                pos,
                system,
                gridpos,
                title,
                axislabels,
                limits,
                extra=0):
    if type == "bisection":
        return Bisection_plot(pos, system, gridpos, title, axislabels, limits)
    elif type == "newtons":
        return Newton_plot(pos, system, gridpos, title, axislabels, limits)
    elif type == "fixed_point":
        return Fixed_point_plot(pos, system, gridpos, title, axislabels,
                                limits, extra)


class System:

    def __init__(self, dt, save, saveAs=r"./animation.gif"):
        self.dt = dt
        self.save = save
        self.saveAs = saveAs

        self.fig = plt.figure(figsize=(16, 9))
        self.fig.suptitle("Figure Title")
        self.plots = []
        self.t = [0]  # time

        plt.subplots_adjust(hspace=0.648, top=0.943, bottom=0.08)
        plt.style.use("dark_background")
        self.fig.patch.set_facecolor("black")
        self.fig.tight_layout()

        grid = self.fig.add_gridspec(6, 4)

        self.plots.append(
            create_plot("newtons", 3, self, grid[0:6, 0:4],
                        "Newtons Method Visualization", ["X", "Y"],
                        [[-2, 3], [-10, 10]]))

        # self.plots.append(
        #     create_plot("bisection", 3, self, grid[0:4, 0:4],
        #                 "Bisection Method Visualization", ["X", "Y"],
        #                 [[-2, 3], [-10, 10]]))

        # self.plots.append(
        #     create_plot("newtons", 3, self, grid[0:2, 0:4],
        #                 "Newtons Method Visualization", ["X", "Y"],
        #                 [[-2, 3], [-10, 10]]))

        # self.plots.append(
        #     create_plot("bisection", 3, self, grid[2:4, 0:4],
        #                 "Bisection Method Visualization", ["X", "Y"],
        #                 [[-2, 3], [-10, 10]]))

        def g1(x):
            return np.sqrt(2 * x + 3)

        def g2(x):
            return (x**2 - 3) / 2

        def g3(x):
            return 3 / (x - 2)

        # self.plots.append(
        #     create_plot("fixed_point", 3, self, grid[0:2, 0:4], "g1",
        #                 ["X", "Y"], [[-2, 3], [-10, 10]], g1))

        # self.plots.append(
        #     create_plot("fixed_point", 3, self, grid[2:4, 0:4], "g2",
        #                 ["X", "Y"], [[-2, 3], [-10, 10]], g2))

        # self.plots.append(
        #     create_plot("fixed_point", 3, self, grid[4:6, 0:4], "g3",
        #                 ["X", "Y"], [[-2, 3], [-10, 10]], g3))

        # self.plots.append(
        #     create_plot("fixed_point", 3, self, grid[0:6, 0:4], "g3",
        #                 ["X", "Y"], [[-2, 3], [-10, 10]], g3))

    def update_plots(self):
        ret_ = []
        for _, plot in enumerate(self.plots):
            if type(plot) is Bisection_plot or type(
                    plot) is Newton_plot or type(plot) is Fixed_point_plot:
                ret_ += plot.update(self.t)
        return ret_

    def animate(self, framenum):
        print(framenum)
        iterperframe = 1
        for _ in range(iterperframe):
            self.t.append(framenum * self.dt)
            ret_ = []
            ret_ += self.update_plots()

        return ret_

    def run(self):
        # kjører animasjon i matplotlib
        self.animation = animation.FuncAnimation(
            self.fig,
            self.animate,
            fargs=(),
            interval=1,
            frames=200,
        )

        if self.save:
            self.save_as_gif()
        plt.show()

    def save_as_gif(self):
        # saves animation as gif using ffmpeg and outputs to specified location
        writer = animation.FFMpegWriter(fps=60, bitrate=18_000)
        self.animation.save(self.saveAs, writer=writer)


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
    hex_codes = [
        '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
        for r, g, b in rgb
    ]
    return hex_codes


if __name__ == "__main__":

    # dt, save
    system = System(2, True)
    system.run()
