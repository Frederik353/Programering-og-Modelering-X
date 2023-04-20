#! /usr/bin/env python

import sim

import numpy as np


class FemtenKuleTrekant(object):
    # posisjonerer kuleene i en trekant som start formasjonen
    def __init__(self, kuler, spacing_factor=1e-3):
        self.kuler = kuler
        self.radius = max([kule.R for kule in self.kuler])
        self.spacer = spacing_factor * self.radius
        self.eff_radius = self.radius + self.spacer + sim.toleranse

        if len(self.kuler) != 15:
            raise ValueError("Trenger 15 kuler")

    def arrange(self):
        a = np.sqrt(3)
        r = self.eff_radius

        def add_space(xyz): 
            rad = self.spacer*1e7
            return xyz + np.array([rad, rad, 0])

        self.kuler[0].svw[0] = add_space(np.array([0, 0, 0]))

        self.kuler[1].svw[0] = add_space(np.array([-r, a*r, 0]))
        self.kuler[2].svw[0] = add_space(np.array([+r, a*r, 0]))

        self.kuler[3].svw[0] = add_space(np.array([-2*r, 2*a*r, 0]))
        self.kuler[4].svw[0] = add_space(np.array([0, 2*a*r, 0]))
        self.kuler[5].svw[0] = add_space(np.array([+2*r, 2*a*r, 0]))

        self.kuler[6].svw[0] = add_space(np.array([-r, 3*a*r, 0]))
        self.kuler[7].svw[0] = add_space(np.array([+r, 3*a*r, 0]))
        self.kuler[8].svw[0] = add_space(np.array([+3*r, 3*a*r, 0]))
        self.kuler[9].svw[0] = add_space(np.array([-3*r, 3*a*r, 0]))

        self.kuler[10].svw[0] = add_space(np.array([2*r, 4*a*r, 0]))
        self.kuler[11].svw[0] = add_space(np.array([-2*r, 4*a*r, 0]))
        self.kuler[12].svw[0] = add_space(np.array([-4*r, 4*a*r, 0]))
        self.kuler[13].svw[0] = add_space(np.array([4*r, 4*a*r, 0]))
        self.kuler[14].svw[0] = add_space(np.array([0, 4*a*r, 0]))

    def senter(self, x, y):
        # sentrerer trekanten med kuler rundt koordinatet (x, y)
        for kule in self.kuler:
            kule.svw[0,0] += x
            kule.svw[0,1] += y

    def sentrer_på_bord(self, bord):
        # sentrerer trekant på bordet
        x = bord.w/2
        y = bord.l*6/8
        self.senter(x, y)
