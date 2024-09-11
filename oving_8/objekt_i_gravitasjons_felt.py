from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import time
import random


class System:
    def __init__(self, p, v, a, rho, tau, boundry, t=[0, 0, 0], radius=1):
        # Initial values
        self.p = p
        self.v = v
        self.a = a
        self.t = t
        self.freefall = [True, True, True]  # state: freefall or in contact
        self.rho = rho     # coefficient of restitution
        self.tau = tau     # contact time for bounce (s)
        self.vmax = [0, 0, 0]
        self.v_imp = [0, 0, 0]
        self.t_hit = [0, 0, 0]  # time of last impact
        self.t_bounce = [0, 0, 0]  # time of next bounce

        self.time_data, self.pos_data, self.vel_data = [[t[0]], [t[1]], [t[2]]], [
            [p[0]], [p[1]], [p[2]]], [[v[0]], [v[1]], [v[2]]]
        self.radius = radius  # radius of ball
        self.compression = [0, 0, 0]
        self.boundry = boundry  # boundrys of ball

        self.m1, self.m2 = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]

    def update(self):
        global time_interval
        dt = (time.time() - time_interval)
        time_interval = time.time()

        for i, p in enumerate(self.p):

            hnew = p + self.v[i]*dt + (1/2)*self.a[i]*dt**2
            if(self.freefall[i]):
                if(hnew < self.boundry[i][0] or hnew > self.boundry[i][1]):  # has impacted
                    self.t_hit[i] = (-self.p[i] + hnew +
                                     self.t[i]*self.v[i])/self.v[i]

                    self.vmax[i] = -(self.v[i] - self.a[i] *
                                     (self.t_hit[i] - self.time_data[i][-1])) * self.rho
                    # print(self.vmax[i]/0.75, i)

                    if hnew < self.boundry[i][0]:
                        # assumes no movment between impact and rebounce
                        self.pos_data[i].extend(
                            [self.boundry[i][0], self.boundry[i][0]])
                        self.p[i] = self.boundry[i][0]
                    else:
                        self.p[i] = self.boundry[i][1]
                        self.pos_data[i].extend(
                            [self.boundry[i][1], self.boundry[i][1]])

                    self.time_data[i].append(self.t_hit[i])
                    self.vel_data[i].extend([0, 0])
                    self.v[i] = 0
                    self.t_bounce[i] = self.t_hit[i] + self.tau
                    self.t[i] += dt
                    self.time_data[i].append(self.t[i])
                    self.freefall[i] = False

                else:  # normal freefall
                    self.t[i] += dt
                    self.time_data[i].append(self.t[i])
                    self.v[i] += self.a[i] * dt
                    self.vel_data[i].append(self.v[i])
                    self.p[i] = hnew
                    self.pos_data[i].append(hnew)
            else:
                if (self.t[i] + dt) >= self.t_bounce[i]:  # if should have bounced
                    self.time_data[i].append(self.t_bounce[i])
                    self.v[i] = self.vmax[i]
                    self.vel_data[i].append(self.v[i])
                    self.pos_data[i].append(self.pos_data[i][-1])
                    self.t[i] += dt  # find vars at time = now
                    self.time_data[i].append(self.t[i])
                    self.p[i] = hnew
                    self.pos_data[i].append(hnew)
                    self.v[i] += self.a[i]*dt
                    self.vel_data[i].append(self.v[i])
                    self.freefall[i] = True
                else:  # if still in bounce procces
                    self.t[i] += dt
                    self.time_data[i].append(self.t[i])
                    self.pos_data[i].append(self.pos_data[i][-1])
                    self.vel_data[i].append(0)


def animate(i):
    global ball, time_interval, sphere, trajectory

    sim_time = time.time() - start_time
    sim_time_label.set_text("Simulation Time: " + str(round(sim_time, 2)))

    spr = 30  # sec per runde
    angle = sim_time * 360 / spr
    print(angle, sim_time)
    ax[2].view_init(30, angle)

    ball.update()

    if sphere:
        ax[2].collections.remove(sphere)
    # if trajectory:
        # ax[2].collections.remove(trajectory)

    # parameter fremsitilling av en kule
    x = ball.p[0] + ball.radius * np.cos(ball.m1)*np.sin(ball.m2)
    y = ball.p[1] + ball.radius * np.sin(ball.m1)*np.sin(ball.m2)
    z = ball.p[2] + ball.radius * np.cos(ball.m2)
    sphere = ax[2].plot_wireframe(
        x, y, z,  rstride=1, cstride=1, color='b', linewidth=0.25)
    # trajectory = ax[2].plot3D( ball.pos_data[0], ball.pos_data[1], ball.pos_data[2])

    vel_vector.set_segments([[[ball.p[0], ball.p[1], ball.p[2]], [
                            ball.p[0] + ball.v[0], ball.p[1] + ball.v[1], ball.p[2] + ball.v[2]]]])

    for i, p in enumerate(ball.p):
        pos_plot[i].set_data(ball.time_data[i], ball.pos_data[i])
        vel_plot[i].set_data(ball.time_data[i], ball.vel_data[i])

    ret_ = [sim_time_label, ax[2]] + vel_plot + pos_plot
    return ret_


# def init_func():
#     ret_ = [sim_time_label] + vel_plot + pos_plot
#     return ret_


def init_plots(plot, xmin, xmax, ymin, ymax, xlabel, ylabel, title, color):
    ax[plot].set_xlim((xmin, xmax))
    ax[plot].set_ylim((ymin, ymax))
    ax[plot].set_xlabel(xlabel)
    ax[plot].set_ylabel(ylabel)
    # ax[plotx, ploty].grid()
    if plot != 2:
        ax[plot].axhline(y=0, linewidth=0.7, color='k')
    # ax[plotx,ploty].legend()
    ax[plot].set_title(title)


if __name__ == "__main__":

    # g = -9.81
    g = -1.625
    boundry = [[-20, 20], [-20, 20], [0, 40]]
    simulation_time = 30.0
    plot_border = 1.1
    # [x, y ,z]
    # p, v, a, rho, tau, t=0
    ball = System([0, 0, 20], [10, -10, 10], [0, 0, g], 0.75, 0.10, boundry)
    # ball = System([random.randint(boundry[0][0], boundry[0][1]), random.randint(boundry[1][0], boundry[1][1]), random.randint(boundry[1][0], boundry[1][1])], [ random.randint(-30, 30), random.randint(-30, 30), random.randint(-30, 30)], [random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1)], random.randint(5, 8)/10, 0.10, boundry)
    # vill miste så mange punker at grafen vil ha feil kurve med for høy fart, pga programmet kjører i realtime og rekker ikke holde opp med farten
    sphere = None
    trajectory = None

    fig = plt.figure(figsize=(13, 8))
    fig.tight_layout()
    ax = []

    grid = fig.add_gridspec(2, 3)
    # ax.append(fig.add_subplot(shape=(2, 3), loc=(0, 0), colspan=1, rowspan=1))
    ax.append(fig.add_subplot(grid[0, 0:1]))
    ax.append(fig.add_subplot(grid[1:, 0:1]))
    ax.append(fig.add_subplot(grid[0:2, 1:3], projection="3d"))

    # fig.add_subplot(2, 1, 1)
    # ax.append(fig.add_subplot(2, 2, 1))
    # ax.append(fig.add_subplot(2, 2, 2))
    # ax.append(fig.add_subplot(2, 2, 3))
    # ax.append(fig.add_subplot(2, 2, 4, projection='3d'))
    plt.subplots_adjust(hspace=0.3)

    # plotx, ploty, xmin,xmax,ymin,ymax,xlabel, ylabel, title, color
    init_plots(0, 0, simulation_time, np.min(boundry) * plot_border,
               np.max(boundry)*plot_border, "Time: (s)", "Position", "Position Plot", "g")

    foo = []
    for i, v in enumerate(ball.v):
        a = ball.a[i]
        p = ball.p[i]
        # if v > (boundry[i][0] + (boundry[i][1] - boundry[i][0])):
        # delta_s = abs(boundry[i][1] - p)
        if a != 0:
            # if first hit upper bound
            if (v**2 / (2 * a)) + p > boundry[i][1]:
                delta_s = boundry[i][1] - p
                foo.append(np.sqrt(v**2+abs(2*a * delta_s)))
            else:
                delta_s = p - boundry[i][0]
                # print(v, a, delta_s)
                foo.append(-np.sqrt(v**2+abs(2*a * delta_s)))
        else:
            if v > 0:  # if first hit upper bound
                delta_s = abs(boundry[i][1] - p)
                foo.append(v)
            else:
                delta_s = -abs(boundry[i][0] - p)
                foo.append(-v)

    v_bound = [np.max(foo), np.min(foo), -np.max(foo) *
               ball.rho, -np.min(foo) * ball.rho]

    init_plots(1, 0, simulation_time, np.min(v_bound) * plot_border,
               np.max(v_bound)*plot_border, "Time: (s)", "Velocity ", "Velocity Plot", "b")

    # init_plots(2, 0, simulation_time, -30, 30, "Time: (s)", "Acceleration", "Acceleration Plot", "r")

    sim_time_label = ax[2].text2D(0, 0.95, '', transform=ax[2].transAxes)

    pos_plot, vel_plot = [], []
    for i, p in enumerate(ball.p):
        pos_plot.append(ax[0].plot([], [], label="")[0])
        vel_plot.append(ax[1].plot([], [],)[0])

    init_plots(2, boundry[0][0], boundry[0][1], boundry[1][0],
               boundry[1][1], "Y position", "X position", "Animation", None)
    ax[2].set_zlim(boundry[2][0], boundry[2][1])
    ax[2].set_zlabel("Z position")

    start_time = time.time()
    time_interval = start_time
    vel_vector = ax[2].quiver(0, 0, 0, 0, 0, 0)

    animate = animation.FuncAnimation(
        fig, animate, interval=0.01, blit=True)

    plt.show()
