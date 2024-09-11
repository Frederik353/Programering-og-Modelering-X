import math
import random
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from vectors import Vector


class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class body:
    def __init__(self, location, mass, velocity, name=""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name


# def partial_step(point1, point2, time_step):
#     ret = point(0, 0, 0)
#     ret.x = point1.x + point2.x * time_step
#     ret.y = point1.y + point2.y * time_step
#     ret.z = point1.z + point2.z * time_step
#     return ret

def partial_step(point1, point2, time_step):
    ret = [0, 0, 0]
    ret[0] = point1[0] + point2[0] * time_step
    ret[1] = point1[1] + point2[1] * time_step
    ret[2] = point1[2] + point2[2] * time_step
    return ret


class RK4_integrator:
    def __init__(self, time_step, bodies):
        self.time_step = time_step
        self.bodies = bodies

    def calculate_single_body_acceleration(self, body_index):
        G_const = 6.67408e-11  # m3 kg-1 s-2
        acceleration = point(0, 0, 0)
        target_body = self.bodies[body_index]

        k1 = [0, 0, 0]
        k2 = [0, 0, 0]
        k3 = [0, 0, 0]
        k4 = [0, 0, 0]
        tmp_loc = [0, 0, 0]
        tmp_vel = [0, 0, 0]

        for index, external_body in enumerate(self.bodies):
            if index != body_index:
                r = (target_body.position[0] - external_body.position[0])**2 + (target_body.position[1] -
                                                                                external_body.position[1])**2 + (target_body.position[2] - external_body.position[2])**2
                r = math.sqrt(r)

                tmp = G_const * external_body.mass / r**3

                # k1 - regular Euler acceleration
                k1[0] = tmp * (external_body.position[0] -
                               target_body.position[0])
                k1[1] = tmp * (external_body.position[1] -
                               target_body.position[1])
                k1[2] = tmp * (external_body.position[2] -
                               target_body.position[2])

                # k2 - acceleration 0.5 timesteps in the future based on k1 acceleration value
                tmp_vel = partial_step(target_body.velocity, k1, 0.5)
                tmp_loc = partial_step(
                    target_body.position, tmp_vel, 0.5 * self.time_step)
                k2[0] = (external_body.position[0] - tmp_loc[0]) * tmp
                k2[1] = (external_body.position[1] - tmp_loc[1]) * tmp
                k2[2] = (external_body.position[2] - tmp_loc[2]) * tmp

                # k3 acceleration 0.5 timesteps in the future using k2 acceleration
                tmp_vel = partial_step(target_body.velocity, k2, 0.5)
                tmp_loc = partial_step(
                    target_body.position, tmp_vel, 0.5 * self.time_step)
                k3[0] = (external_body.position[0] - tmp_loc[0]) * tmp
                k3[1] = (external_body.position[1] - tmp_loc[1]) * tmp
                k3[2] = (external_body.position[2] - tmp_loc[2]) * tmp

                # k4 - location 1 timestep in the future using k3 acceleration
                tmp_vel = partial_step(target_body.velocity, k3, 1)
                tmp_loc = partial_step(
                    target_body.position, tmp_vel, self.time_step)
                k4[0] = (external_body.position[0] - tmp_loc[0]) * tmp
                k4[1] = (external_body.position[1] - tmp_loc[1]) * tmp
                k4[2] = (external_body.position[2] - tmp_loc[2]) * tmp

                acceleration.x += (k1[0] + k2[0] * 2 + k3[0] * 2 + k4[0]) / 6
                acceleration.y += (k1[1] + k2[1] * 2 + k3[1] * 2 + k4[1]) / 6
                acceleration.z += (k1[2] + k2[2] * 2 + k3[2] * 2 + k4[2]) / 6

        return acceleration

    def update_location(self):
        for target_body in self.bodies:
            target_body.position[0] += target_body.position[0] * self.time_step
            target_body.position[1] += target_body.position[1] * self.time_step
            target_body.position[2] += target_body.position[2] * self.time_step

    def compute_velocity(self):
        for body_index, target_body in enumerate(self.bodies):
            acc = self.calculate_single_body_acceleration(body_index)
            acceleration = Vector((acc.x, acc.y, acc.z))
            target_body.velocity += acceleration * self.time_step
            # target_body.velocity[0] += acceleration.x * self.time_step
            # target_body.velocity[1] += acceleration.y * self.time_step
            # target_body.velocity[2] += acceleration.z * self.time_step

    def update_location(self):
        for target_body in self.bodies:
            target_body.position = (
                target_body.position[0] +target_body.velocity[0]  * self.time_step,
                target_body.position[1] + target_body.velocity[1] * self.time_step,
                target_body.position[2] + target_body.velocity[2]* self.time_step
            )

    def compute_gravity_step(self):
        self.compute_velocity()
        self.update_location()


def run_simulation(integrator, names=None, number_of_steps=10000, report_freq=100):

    body_locations_hist = []
    for current_body in bodies:
        body_locations_hist.append(
            {"x": [], "y": [], "z": [], "name": current_body.name})

    for i in range(0, int(number_of_steps)):
        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index].position[0])
                body_location["y"].append(bodies[index].position[0])
                body_location["z"].append(bodies[index].position[0])
        integrator.compute_gravity_step()

    return body_locations_hist


if __name__ == "__main__":
    import config

    config.main()


class Euler_integrator:
    def __init__(self, time_step, bodies):
        self.time_step = time_step
        self.bodies = bodies

    def calculate_single_body_acceleration(self, body_index):
        G_const = 6.67408e-11  # m3 kg-1 s-2
        acceleration = point(0, 0, 0)
        target_body = self.bodies[body_index]
        for index, external_body in enumerate(bodies):
            if index != body_index:
                r = (target_body.location.x - external_body.location.x)**2 + (target_body.location.y -
                                                                              external_body.location.y)**2 + (target_body.location.z - external_body.location.z)**2
                r = math.sqrt(r)
                tmp = G_const * external_body.mass / r**3
                acceleration.x += tmp * \
                    (external_body.location.x - target_body.location.x)
                acceleration.y += tmp * \
                    (external_body.location.y - target_body.location.y)
                acceleration.z += tmp * \
                    (external_body.location.z - target_body.location.z)

        return acceleration

    def update_location(self):
        for target_body in self.bodies:
            target_body.location.x += target_body.velocity.x * self.time_step
            target_body.location.y += target_body.velocity.y * self.time_step
            target_body.location.z += target_body.velocity.z * self.time_step

    def compute_velocity(self):
        for body_index, target_body in enumerate(self.bodies):
            acceleration = self.calculate_single_body_acceleration(body_index)
            target_body.velocity.x += acceleration.x * self.time_step
            target_body.velocity.y += acceleration.y * self.time_step
            target_body.velocity.z += acceleration.z * self.time_step

    def update_location(self):
        for target_body in self.bodies:
            target_body.location.x += target_body.velocity.x * self.time_step
            target_body.location.y += target_body.velocity.y * self.time_step
            target_body.location.z += target_body.velocity.z * self.time_step

    def compute_gravity_step(self):
        self.compute_velocity()
        self.update_location()
