import sim.animering

from sim.animering import *

import pygame
import pygame.gfxdraw

from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    K_DOWN,
    K_UP,
    K_RIGHT,
    K_LEFT,
    K_r,
    KEYDOWN,
    KEYUP,
    QUIT,
)

import numpy as np


class Kule(pygame.sprite.Sprite):
    # kule i pygame

    def __init__(self, kule, svw_log, scale, offset_x=0, offset_y=0, spor=True):
        self.scale = scale
        self.id = kule.id
        self._kule = kule
        self.radius = d_to_px(kule.R, self.scale)

        self.svw_log = svw_log
        self.xs = d_to_px(scale, self.svw_log[:,0,0], offset_x)
        self.ys = d_to_px(scale, self.svw_log[:,0,1], offset_y)

        super(Kule, self).__init__()

        self.farge = KULE_FARGER.get(self.id, (255,255,255))

        self.spor = spor
        self.spor_lengde = SPOR_LENGDE

        self.surf = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(
            self.surf,
            self.farge,
            (self.radius, self.radius),
            self.radius
        )
        self.rect = self.surf.get_rect()

        self.oppdater(frame=0)


    def oppdater(self, frame):
        # oppdaterer posisjonen
        self.rect.center = (
            self.xs[frame],
            self.ys[frame],
        )


class AnimerSkudd(object):
    # animerer skuddet i pygame

    def __init__(self, shot):
        self.størrelse = MAX_SCREEN
        self.cloth_color = STOFF_FARGE
        self.vegg_color = VEGG_STOFF_FARGE
        self.edge_color = BORD_KANT_FARGE

        self.shot = shot
        self.bord = shot.bord
        self.kuler = shot.kuler
        self.tids = shot.log['tid']

        self.num_frames = shot.n

        self.bord_x, self.bord_y = self.finn_bord_størrelse()
        self.surface_x, self.surface_y = self.finn_spille_flate()
        self.scale = self.størrelse / max([self.bord_x, self.bord_y])

        self.px = {
            'vegg': d_to_px(self.scale, self.bord.vegg_bredde),
            'edge': d_to_px(self.scale, self.bord.edge_width),
            'bord_x': d_to_px(self.scale, self.bord_x),
            'bord_y': d_to_px(self.scale, self.bord_y),
            'surface_x': d_to_px(self.scale, self.surface_x),
            'surface_y': d_to_px(self.scale, self.surface_y),
            'diamond': d_to_px(self.scale, sim.bord_merke_størrelse),
        }
        self.px['offset_x'] = (self.px['bord_x'] - self.px['surface_x'])/2
        self.px['offset_y'] = (self.px['bord_y'] - self.px['surface_y'])/2

        pygame.init()

        self.screen = pygame.display.set_mode((self.px['bord_x'], self.px['bord_y']))

        self.init_kule_sprites()

        self.clock = pygame.time.Clock()
        self.fps = self.finn_fps()
        self.frame = 0

        self.tilstand = Tilstand()

    def finn_bord_størrelse(self):
        # total bord størrelse
        return (
            2*self.bord.vegg_bredde + 2*self.bord.edge_width + self.bord.w,
            2*self.bord.vegg_bredde + 2*self.bord.edge_width + self.bord.l,
        )

    def finn_spille_flate(self):
        # spill flate på bord
        return (
            self.bord.w,
            self.bord.l,
        )

    def init_kule_sprites(self):
        # lager kule_sprites

        self.kule_sprites = pygame.sprite.Group()
        for kule_id, kule in self.kuler.items():
            self.kule_sprites.add(Kule(
                kule=kule,
                svw_log=self.shot.log['kuler'][kule_id]["svw"],
                scale=self.scale,
                offset_x=(self.px['vegg'] + self.px['edge']),
                offset_y=(self.px['vegg'] + self.px['edge']),
            ))

    def finn_fps(self):
        return 1/(self.tids[-1] - self.tids[-2])

    def tegn_kule_spor(self):
        # tegner sporene etter kulene
        if self.frame < 2:
            return

        for kule in self.kule_sprites.sprites():
            if not kule.spor:
                continue

            spor_lengde = self.frame if self.frame < kule.spor_lengde else kule.spor_lengde

            for n in range(spor_lengde - 1):
                pygame.gfxdraw.line(
                    self.screen,
                    kule.xs[self.frame - spor_lengde + n],
                    kule.ys[self.frame - spor_lengde + n],
                    kule.xs[self.frame - spor_lengde + n + 1],
                    kule.ys[self.frame - spor_lengde + n + 1],
                    (*kule.farge, 255 * (1 - np.exp(-n/spor_lengde))),
                )


    def tegn_mangekant(self, coords, color):
        pygame.draw.polygon(self.screen, color, coords)


    def tegn_bue(self, x, y, r, start, end, color, n=30):
        start, end = np.deg2rad(start), np.deg2rad(end)
        thetas = np.linspace(start, end, n)
        coords = [(x, y)]
        for theta in thetas:
            coords.append((x + r*np.cos(theta), y + r*np.sin(theta)))

        self.tegn_mangekant(coords, color)


    def tegn_bord(self):
        # tegn bordet
        self.tegn_spillflate()
        self.tegn_vegger_og_bordkanter()


    def tegn_spillflate(self):
        # tegn spillflaten
        self.screen.fill(self.cloth_color)

        # Headstring
        pygame.draw.line(
            self.screen,
            (200,200,200),
            (self.px['edge']+self.px['vegg'], int(1/4*self.px['bord_y'])),
            (self.px['bord_x']-self.px['edge'], int(1/4*self.px['bord_y'])),
        )


    def tegn_vegger_og_bordkanter(self):
        edge = self.px['edge']
        vegg = self.px['vegg']
        tx = self.px['bord_x']
        ty = self.px['bord_y']

        # Bottom edge
        self.tegn_mangekant([(edge, 0), (edge, edge), (tx-edge, edge), (tx-edge, 0)], self.edge_color)
        self.tegn_mangekant([(edge, edge), (edge, edge+vegg), (tx-edge, edge+vegg), (tx-edge, edge)], self.vegg_color)

        # Left edge
        self.tegn_mangekant([(0, edge), (0, ty-edge), (edge, ty-edge), (edge, edge)], self.edge_color)
        self.tegn_mangekant([(edge, edge), (edge, ty-edge), (edge+vegg, ty-edge), (edge+vegg, edge)], self.vegg_color)

        # Right edge
        self.tegn_mangekant([(tx-edge, edge), (tx-edge, ty-edge), (tx, ty-edge), (tx, edge)], self.edge_color)
        self.tegn_mangekant([(tx-edge-vegg, edge), (tx-edge-vegg, ty-edge), (tx-edge, ty-edge), (tx-edge, edge)], self.vegg_color)

        # Top edge
        self.tegn_mangekant([(edge, ty-edge), (edge, ty), (tx-edge, ty), (tx-edge, ty-edge)], self.edge_color)
        self.tegn_mangekant([(edge, ty-edge-vegg), (edge, ty-edge), (tx-edge, ty-edge), (tx-edge, ty-edge-vegg)], self.vegg_color)

        # Corners
        self.tegn_bue(edge, edge, edge, 180, 270, self.edge_color)
        self.tegn_bue(edge, ty-edge, edge, 90, 180, self.edge_color)
        self.tegn_bue(tx-edge, ty-edge, edge, 0, 90, self.edge_color)
        self.tegn_bue(tx-edge, edge, edge, 270, 360, self.edge_color)

        # Diamonds
        D = lambda coords: pygame.draw.circle(self.screen, BORD_MERKE_FARGE, coords, self.px['diamond'])

        for i in range(9):
            y_val = int(edge/2 + (ty - edge)*i/8)
            D((int(edge/2), y_val))
            D((tx - int(edge/2), y_val))

        for i in range(5):
            x_val = int(edge/2 + (tx - edge)*i/4)
            D((x_val, int(edge/2)))
            D((x_val, int(ty - edge/2)))


    def display(self):
        # Flip vertical axis so origin is bottom left
        display_surface = pygame.display.get_surface()
        display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))

        # Update the display
        pygame.display.flip()


    def tegn_kuler(self):
        # Draw the kuler on the screen
        for kule in self.kule_sprites:
            self.screen.blit(kule.surf, kule.rect)


    def oppdater_kuler(self, frame):
        for kule in self.kule_sprites:
            kule.oppdater(frame=frame)


    def hondter_hendelser(self):
        if not self.tilstand.paused:
            self.oppdater_kuler(self.frame)
            self.frame += 1

        elif self.tilstand.frame_backward:
            self.frame -= 1
            self.oppdater_kuler(self.frame)

        elif self.tilstand.frame_forward:
            self.frame += 1
            self.oppdater_kuler(self.frame)

        if self.frame >= self.num_frames:
            # Restart animation
            self.frame = 0

        if self.tilstand.restart:
            # Restart animation
            self.frame = 0

        if self.tilstand.decrease_speed:
            self.fps = max([1, self.fps*0.96])
        elif self.tilstand.increase_speed:
            self.fps = min([30, self.fps*1.04])


    def start(self):
        while self.tilstand.running:
            self.tilstand.oppdater()
            self.tegn_bord()
            self.tegn_kuler()
            self.tegn_kule_spor()
            self.display()
            self.hondter_hendelser()
            self.clock.tick(self.fps)


class Tilstand(object):
    def __init__(self):
        self.running = True
        self.paused = False
        self.frame_forward = False
        self.frame_backward = False
        self.increase_speed = False
        self.decrease_speed = False
        self.restart = False


    def oppdater(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.running = False
                elif event.key == K_SPACE: self.paused = not self.paused
                elif event.key == K_DOWN: self.decrease_speed = True
                elif event.key == K_UP: self.increase_speed = True
                elif event.key == K_RIGHT: self.paused = True; self.frame_forward = True
                elif event.key == K_LEFT: self.paused = True; self.frame_backward = True
                elif event.key == K_r: self.restart = True
            elif event.type == KEYUP:
                if event.key == K_DOWN: self.decrease_speed = False
                elif event.key == K_UP: self.increase_speed = False
                elif event.key == K_RIGHT: self.frame_forward = False
                elif event.key == K_LEFT: self.frame_backward = False
                elif event.key == K_r: self.restart = False
            elif event.type == QUIT:
                self.running = False


