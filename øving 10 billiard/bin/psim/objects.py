import psim
import psim.utils as utils
import psim.physics as physics

import numpy as np

from functools import partial


class Ball(object):
    def __init__(self, ball_id, m=None, R=None):
        self.id = ball_id

        # physical properties
        self.m = m or psim.m
        self.R = R or psim.R
        self.I = 2/5 * self.m * self.R**2

        self.svw = np.array([[np.nan, np.nan, np.nan],  # positions (r)
                             [0,      0,      0],  # velocities (v)
                             [0,      0,      0],  # angular velocities (w)
                             [0,      0,      0]])  # angular integrations (e)

        # stille=0, spinnende=1, glidende=2, rullende=3
        self.s = 0

    def set(self, svw, s):
        self.s = s
        self.svw = svw


class Table(object):
    def __init__(self, w=None, l=None, u_g=None, u_r=None, u_sp=None,
                 edge_width=None, vegg_bredde=None, vegg_høyde=None,
                lights_height=None):

        self.w = w or psim.bord_bredde
        self.l = l or psim.bord_lengde
        self.edge_width = edge_width or psim.bord_kant_bredde
        self.vegg_bredde = vegg_bredde or psim.vegg_bredde  # for visualization

        self.L = 0
        self.R = self.w
        self.B = 0
        self.T = self.l

        self.center = (self.w/2, self.l/2)

        # felt properties
        self.u_g = u_g or psim.u_g
        self.u_r = u_r or psim.u_r
        self.u_sp = u_sp or psim.u_sp

        self.rails = {
            'L': Rail('L', lx=1, ly=0, l0=-self.L, height=vegg_høyde),
            'R': Rail('R', lx=1, ly=0, l0=-self.R, height=vegg_høyde),
            'B': Rail('B', lx=0, ly=1, l0=-self.B, height=vegg_høyde),
            'T': Rail('T', lx=0, ly=1, l0=-self.T, height=vegg_høyde),
        }


class Rail(object):
    """A rail is defined by a line lx*x + ly*y + l0 = 0"""

    def __init__(self, rail_id, lx, ly, l0, height=None):
        self.id = rail_id

        self.lx = lx
        self.ly = ly
        self.l0 = l0

        # Defines the normal vector of the rail surface
        self.normal = np.array([self.lx, self.ly, 0])

        # rail properties
        self.height = height or psim.vegg_høyde


class Cue(object):
    def __init__(self, M=psim.M):
        self.M = M

    def strike(self, ball, V0, phi, theta=None, a=None, b=None):

        v, w = physics.cue_strike(ball.m, self.M, ball.R, V0, phi, theta, a, b)
        svw = np.array([ball.svw[0], v, w, ball.svw[3]])

        s = (psim.rullende
             if abs(np.sum(physics.get_rel_velocity(svw, ball.R))) <= psim.toleranse
             else psim.glidende)

        ball.set(svw, s)

    def strike_object(self, ball, V0, obj, offset=0, theta=None, a=None, b=None):
        """Strike a ball to another object that has an svw. FIXME"""

        phi = utils.angle(obj.svw[0] - ball.svw[0]) * 180/np.pi + offset

        v, w = physics.cue_strike(ball.m, self.M, ball.R, V0, phi, theta, a, b)
        svw = np.array([ball.svw[0], v, w, ball.svw[3]])

        s = (psim.rullende
             if abs(np.sum(physics.get_rel_velocity(svw, ball.R))) <= psim.toleranse
             else psim.glidende)

        ball.set(svw, s)
