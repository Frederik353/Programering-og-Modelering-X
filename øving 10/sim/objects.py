import sim
import sim.utils as utils
import sim.physics as physics

import numpy as np

from functools import partial


class Kule(object):
    def __init__(self, kule_id ):
        self.id = kule_id

        # kule masse, radius
        self.m = sim.m
        self.R = sim.R

        self.svw = np.array([[np.nan, np.nan, np.nan],  # posisjon (s)
                             [0,      0,      0],  # fartsvektor (v)
                             [0,      0,      0],  # vinkelmomenter (w)
                             [0,      0,      0]])  # vinkel integral (e)

        # stille=0, spinnenende=1, glidende=2, rullende=3
        self.s = 0

    def set(self, svw, s):
        # oppdaterer kulen
        self.s = s
        self.svw = svw


class Bord(object):
    # lager ett bord
    def __init__(self):

        self.w = sim.bord_bredde
        self.l = sim.bord_lengde
        self.edge_width = sim.bord_kant_bredde
        self.vegg_bredde = sim.vegg_bredde # brukt til visualiseringen

        self.L = 0 # venstre vegg
        self.R = self.w # høyre vegg
        self.B = 0 # nedre vegg
        self.T = self.l # øvre vegg

        self.senter = (self.w/2, self.l/2) # senterpunktet til bordet

        # friksjonskoeffisienter til bordet i de gjeldende ball tilstandene
        self.u_g = sim.u_g
        self.u_r = sim.u_r
        self.u_sp = sim.u_sp

        # setter opp veggene 
        self.veggs = {
            'L': Vegg('L', lx=1, ly=0, l0=-self.L),
            'R': Vegg('R', lx=1, ly=0, l0=-self.R),
            'B': Vegg('B', lx=0, ly=1, l0=-self.B),
            'T': Vegg('T', lx=0, ly=1, l0=-self.T),
        }


class Vegg(object):
    def __init__(self, vegg_id, lx, ly, l0):
        self.id = vegg_id

        self.lx = lx
        self.ly = ly
        self.l0 = l0

        # normalvektoren til veggen
        self.normal = np.array([self.lx, self.ly, 0])

        self.height = sim.vegg_høyde


class Billiardkølle(object):
    def __init__(self, M=sim.M):
        self.M = M

    def skudd(self, kule, V0, phi, theta=None, a=None, b=None):

        v, w = physics.stav_skudd(kule.m, self.M, kule.R, V0, phi, theta, a, b)
        svw = np.array([kule.svw[0], v, w, kule.svw[3]])

        s = (sim.rullende if abs(np.sum(physics.finn_rel_velocity(svw, kule.R))) <= sim.toleranse else sim.glidende)

        kule.set(svw, s)

    def skudd_treff_kule(self, kule, V0, obj, offset=0, theta=None, a=None, b=None):
        # skyt en kule borti et objekt/kule

        phi = utils.angle(obj.svw[0] - kule.svw[0]) * 180/np.pi + offset

        v, w = physics.stav_skudd(kule.m, self.M, kule.R, V0, phi, theta, a, b)
        svw = np.array([kule.svw[0], v, w, kule.svw[3]])

        s = (sim.rullende
             if abs(np.sum(physics.finn_rel_velocity(svw, kule.R))) <= sim.toleranse
             else sim.glidende)

        kule.set(svw, s)
