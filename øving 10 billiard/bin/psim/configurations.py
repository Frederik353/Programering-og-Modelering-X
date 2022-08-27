#! /usr/bin/env python

import psim

from psim.objects import Ball

import numpy as np


class FifteenBallRack(object):
    """Arrange a list of balls into 9-ball break configuration"""
    def __init__(self, balls, spacing_factor=1e-3, ordered=False):
        self.balls = balls
        self.radius = max([ball.R for ball in self.balls])
        self.spacer = spacing_factor * self.radius
        self.eff_radius = self.radius + self.spacer + psim.toleranse

        if len(self.balls) != 15:
            raise ValueError("NineBallRack :: must pass exactly 9 balls")

        if not ordered:
            self.balls = np.random.choice(self.balls, replace=False, size=len(self.balls))


    def arrange(self):
        a = np.sqrt(3)
        r = self.eff_radius

        def add_space(xyz):
            rad = self.spacer*np.random.rand()
            return xyz + np.array([rad, rad, 0])

        self.balls[0].svw[0] = add_space(np.array([0, 0, 0]))

        self.balls[1].svw[0] = add_space(np.array([-r, a*r, 0]))
        self.balls[2].svw[0] = add_space(np.array([+r, a*r, 0]))

        self.balls[3].svw[0] = add_space(np.array([-2*r, 2*a*r, 0]))
        self.balls[4].svw[0] = add_space(np.array([0, 2*a*r, 0]))
        self.balls[5].svw[0] = add_space(np.array([+2*r, 2*a*r, 0]))

        self.balls[6].svw[0] = add_space(np.array([-r, 3*a*r, 0]))
        self.balls[7].svw[0] = add_space(np.array([+r, 3*a*r, 0]))
        self.balls[8].svw[0] = add_space(np.array([+3*r, 3*a*r, 0]))
        self.balls[9].svw[0] = add_space(np.array([-3*r, 3*a*r, 0]))

        self.balls[10].svw[0] = add_space(np.array([2*r, 4*a*r, 0]))
        self.balls[11].svw[0] = add_space(np.array([-2*r, 4*a*r, 0]))
        self.balls[12].svw[0] = add_space(np.array([-4*r, 4*a*r, 0]))
        self.balls[13].svw[0] = add_space(np.array([4*r, 4*a*r, 0]))
        self.balls[14].svw[0] = add_space(np.array([0, 4*a*r, 0]))


    def center(self, x, y):
        for ball in self.balls:
            ball.svw[0,0] += x
            ball.svw[0,1] += y


    def center_by_table(self, table):
        x = table.w/2
        y = table.l*6/8
        self.center(x, y)
