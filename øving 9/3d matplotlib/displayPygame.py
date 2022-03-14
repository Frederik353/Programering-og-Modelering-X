import sys
import numpy as np
import pygame
from support import import_folder


class displayPygame:
    pause = False
    lockOnTo = None
    draging = False

    def __init__(
        self,
        solar_system,
        displaySizeMeters,
    ):
        pygame.init()
        pygame.display.set_caption('Image')
        self.screen_width = 1200
        self.screen_height = 700
        # self.radiusAdder = 2e10
        self.radiusAdder = 3e11

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()
        self.images = import_folder("./graphics")

        self.solar_system = solar_system
        self.size = displaySizeMeters  # størrelse på universet
        self.pixelUnit = self.size / self.screen_height
        # brukt for å zoome inn og ut, ganger størrelsen på universet med to for å gjøre det mulig å se alle planetene fra perspektivet til de ytterste planetene som krever att resten av planetene ikke er lengere unna en halve skjermen, gitt planetene blir fort mindre enn en pixel avhengiga av radius adder
        self.maxPixelUnit = self.size * 2 / self.screen_height
        self.scale = 1000
        self.offsetHeight = self.pixelUnit * (self.screen_height / 2)
        self.offsetWidth = self.pixelUnit * (self.screen_width / 2)
        self.sprites = []

    def init_objects(self, body, index):
        body.sprite = planetSprite(self, body, index)
        self.sprites.append(body.sprite)
        body.posarr = [[], []]  # lagrer bare 2d

    def resizeScreen(self, e):

        # surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        # if event.type == pygame.VIDEORESIZE:
        old_surface_saved = self.screen
        self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
        self.screen_width = e.w
        self.screen_height = e.h
        # On the next line, if only part of the window
        # needs to be copied, there's some other options.
        self.screen.blit(old_surface_saved, (0, 0))
        del old_surface_saved

    def pauseSim(self):
        self.solar_system.paused = not self.solar_system.paused
        # if self.solar_system.running:
        # self.solar_system.clock()

    def plotOrbits(self):
        def translate(x): return (x + self.offsetWidth) / self.pixelUnit
        for body in self.solar_system.bodies:
            # antar antall posisjoner er lik i alle dimensjoner, og hopper over første posisjon
            for index, pos in enumerate(body.posarr[0][1:]):
                p1 = (translate(body.posarr[0][index - 1]),
                      translate(body.posarr[1][index - 1]))
                p2 = (translate(body.posarr[0][index]),
                      translate(body.posarr[1][index]))
                line = pygame.Surface(p2, pygame.SRCALPHA)
                pygame.draw.line(self.screen, body.color, p1, p2)
                topLeftx = min(p1[0], p2[0])
                topLefty = min(p1[1], p2[1])
                self.screen.blit(line, (topLeftx, topLefty))

        lineSurface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA)
        # line = pygame.draw.line( self.screen, (0, 255, 255), (0, 0), (self.screen_width, self.screen_height))

        # RED = pygame.Color(255, 0, 0)

        # size = (500, 500)

        # image = pygame.Surface(size)
        # pygame.draw.line(image, RED, (0, 0), (500, 500))

        # self.screen.blit(image, (25, 25))

    def updateOrbits(self):
        for body in self.solar_system.bodies:
            body.posarr[0].append(body.position[0])
            body.posarr[1].append(body.position[1])

    def moveCamera(self, centerCoordinate=True, pos=None):
        keys = pygame.key.get_pressed()  # checking pressed keys
        speed = self.pixelUnit * 2
        self.moveOffsetWidth = self.offsetWidth
        self.moveOffsetHeight = self.offsetHeight
        if pos and centerCoordinate:  # put coordinate in center of screen
            self.offsetWidth = self.screen_width * \
                1/2 * self.pixelUnit - pos[0]
            self.offsetHeight = self.screen_height * \
                1/2 * self.pixelUnit - pos[1]
        elif pos:
            self.offsetWidth = pos[0]
            self.offsetHeight = pos[1]

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.offsetHeight += speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.offsetHeight -= speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.offsetWidth += speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.offsetWidth -= speed

        # begrenser mengden det går ann å bevege seg i alle retningene

        # hvis skjermen viser ett omeråde større enn universet
        unviverseSizeWidth = max(
            2 * self.size, self.screen_width * self.maxPixelUnit)
        unviverseSizeHeight = max(
            2 * self.size, self.screen_height * self.maxPixelUnit)

        # nedre grense må kompansere for at skjermposisjonen er definert som øverste venstre hjørne
        self.offsetWidth = max(- unviverseSizeWidth + self.screen_width *
                               self.pixelUnit, min(self.offsetWidth, unviverseSizeWidth))
        self.offsetHeight = max(- unviverseSizeHeight + self.screen_height *
                                self.pixelUnit, min(self.offsetHeight, unviverseSizeHeight))

    def lockOn(self):
        self.moveCamera(
            pos=(self.lockOnTo.position[0], self.lockOnTo.position[1]))

    def dragAndDrop(self):
        x, y = pygame.mouse.get_pos()
        self.offsetWidth -= self.pixelUnit * (self.prevX - x)
        self.offsetHeight -= self.pixelUnit * (self.prevY - y)
        self.prevX = x
        self.prevY = y

    def eventChecker(self):
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.pauseSim()

            elif e.type == pygame.MOUSEBUTTONDOWN:

                if e.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [
                        s for s in self.solar_system.bodies if s.sprite.rect.collidepoint(pos)]
                    if clicked_sprites:
                        self.lockOnTo = clicked_sprites[0]
                    else:
                        self.draging = True
                        self.prevX, self.prevY = pos
                if e.button == 3:
                    self.lockOnTo = None
                if e.button == 4:
                    self.zoom(max(self.scale - 15, 1))
                if e.button == 5:
                    self.zoom(min(self.scale + 15, 1000))
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.draging = False
            elif e.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                self.resizeScreen(e)

    def updatePygame(self, framenum):
        self.screen.fill((0, 0, 0))
        self.eventChecker()
        self.moveCamera()
        self.updateOrbits()
        self.plotOrbits()

        if self.lockOnTo:
            self.lockOn()
        elif self.draging:
            self.dragAndDrop()

        # self.moveCamera(pos=(self.solar_system.bodies[6].position[0] + (self.screen_width / 2) * self.pixelUnit, self.solar_system.bodies[6].position[1] + (self.screen_height*self.pixelUnit / 2)))
        # self.moveCamera(pos=( self.solar_system.bodies[6].position[0],  self.solar_system.bodies[6].position[1]))
        for int, body in enumerate(self.solar_system.bodies):
            body.sprite.update(((body.position[0] + self.offsetWidth) / self.pixelUnit,
                                (body.position[1] + self.offsetHeight) / self.pixelUnit))

        pygame.display.update()
        # self.clock.tick(60)

    def zoom(self, scale):
        prevPixelUnit = self.pixelUnit
        self.scale = scale
        self.pixelUnit = (self.scale / 1000) * self.maxPixelUnit
        for index, body in enumerate(self.solar_system.bodies):
            # må laste bilde på nytt for å hindre rar effekt som kommer av å skalere bildet gjentatte ganger
            # body.sprite.image = self.images[index]
            body.sprite.scale(index)

        # gjør det mulig å some inn på ting
        x, y = pygame.mouse.get_pos()

        x = self.offsetWidth + (x * self.pixelUnit - x * prevPixelUnit)
        y = self.offsetHeight + (y * self.pixelUnit - y * prevPixelUnit)

        self.moveCamera(centerCoordinate=False, pos=(x, y))


class planetSprite(pygame.sprite.Sprite):

    imgSize = width, height = 480, 360

    def __init__(self, pygameWindow, body, index):
        super().__init__()
        self.pygameWindow = pygameWindow
        self.body = body

        # self.import_character_assets()
        # self.frame_index = 0
        # self.image = self.animations['idle'][self.frame_index]
        # self.image =  pygame.image.load()
        self.scale(index)
        self.update((0, 0))

    def update(self, pos):
        self.rect = self.image.get_rect(center=pos)
        self.pygameWindow.screen.blit(self.image, self.rect)

    def scale(self, index):
        # må laste bilde på nytt for å hindre rar effekt som kommer av å skalere bildet gjentatte ganger
        self.image = self.pygameWindow.images[index]
        # newImgSize = tuple( [z * ((self.body.radius / self.pygameWindow.pixelUnit) / self.height) + self.pygameWindow.radiusAdder for z in self.imgSize])
        newImgSize = tuple([z * (((self.body.radius + self.pygameWindow.radiusAdder) / self.pygameWindow.pixelUnit) /
                                 self.height) for z in self.imgSize])
        # print(.newImgSize)
        self.image = pygame.transform.scale(self.image, newImgSize)
        self.rect = self.image.get_rect(center=(0, 0))

    # def move(self):

    # def update(self):

    # def get_input(self):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_RIGHT]:
    #         self.direction.x = 1
    #         self.facing_right = True
    #     elif keys[pygame.K_LEFT]:
    #         self.direction.x = -1
    #         self.facing_right = False
    #     else:
    #         self.direction.x = 0

    #     if keys[pygame.K_SPACE] and self.on_ground:
    #         self.jump()
    #         self.create_jump_particles(self.rect.midbottom)


if __name__ == "__main__":
    import config

    config.main()
