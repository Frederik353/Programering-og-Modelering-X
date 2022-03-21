import sys
from turtle import position
from matplotlib.pyplot import fill
import numpy as np
import pygame
from support import import_folder
from time import time
from copy import deepcopy


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
        pygame.display.set_caption("solar system simulation")
        self.screen_width = 1200
        self.screen_height = 700
        self.radiusAdder = 1e10
        # self.radiusAdder = 0
        # self.radiusAdder = 3e11

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()
        self.images = import_folder("./graphics")

        self.solar_system = solar_system
        self.size = displaySizeMeters  # størrelse på universet
        # self.pixelUnit = self.size / self.screen_height

        self.maxPixelUnit = self.size * 2 / self.screen_height
        self.scale = 1000
        self.pixelUnit = (self.scale / 1000) * self.maxPixelUnit
        # brukt for å zoome inn og ut, ganger størrelsen på universet med to for å gjøre det mulig å se alle planetene fra perspektivet til de ytterste planetene som krever att resten av planetene ikke er lengere unna en halve skjermen, gitt planetene blir fort mindre enn en pixel avhengiga av radius adder
        self.offsetHeight = self.pixelUnit * (self.screen_height / 2)
        self.offsetWidth = self.pixelUnit * (self.screen_width / 2)
        self.sprites = []

        universeSizeWidth = max(2 * self.size, self.screen_width * self.maxPixelUnit) / self.pixelUnit
        universeSizeHeight = max(2 * self.size, self.screen_height * self.maxPixelUnit) / self.pixelUnit

        self.orbits = pygame.Surface(
            (universeSizeWidth, universeSizeHeight), pygame.SRCALPHA)
        self.orbitSizePixels = abs(self.size / self.pixelUnit)

        self.fontSize = 20
        self.font = pygame.font.Font('freesansbold.ttf', self.fontSize)
        self.smallFontSize = 15
        self.smallFont = pygame.font.SysFont("calibri", self.smallFontSize)

        self.boxToScreenRatio = 7
        self.topleftBox = (self.translateX(
            0) - self.orbitSizePixels / 2, self.translateY(0) - self.orbitSizePixels / 2)
        self.plotOrbits()  # initialiserer variablene som trengs i update funksjonen for blitting
        self.updateOrbits()
        self.replotOrbits = False
        self.lastScroll = 0

    def init_objects(self, body, index):
        body.sprite = planetSprite(self, body, index)
        self.sprites.append(body.sprite)

    def translateX(self, x): return (x + self.offsetWidth) / self.pixelUnit

    def translateY(self, y): return (y + self.offsetHeight) / self.pixelUnit

    def updatePygame(self, framenum):
        self.screen.fill((0, 0, 0))
        self.info = []
        # self.debugChunks()
        if not self.replotOrbits:
            self.updateOrbits()
        self.eventChecker()
        self.moveCamera()

        if self.lockOnTo:
            self.lockOn()
        elif self.draging:
            self.dragAndDrop()

        if self.replotOrbits:
            timeSinceScroll = time() - self.lastScroll
            self.info.append(f"timeSinceScroll: {timeSinceScroll}")
            if timeSinceScroll > 1:  # sec
                self.plotOrbits()
                self.replotOrbits = False

        for int, body in enumerate(self.solar_system.bodies):
            x = self.translateX(body.position[0])
            y = self.translateY(body.position[1])
            body.sprite.update(((x, y)))
            self.tag(body, (x, y))

        self.displayInfo()
        pygame.display.update()

    def resizeScreen(self, e):
        old_surface_saved = self.screen
        self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
        self.screen_width = e.w
        self.screen_height = e.h
        self.screen.blit(old_surface_saved, (0, 0))
        del old_surface_saved

    def pauseSim(self):
        self.solar_system.paused = not self.solar_system.paused

    def get_offsets(self, dist, size):

        # ndim = len(p)
        ndim = 2

        # generate an (m, ndims) array containing all strings over the alphabet {0, 1, 2}:
        offset_idx = np.indices((size,) * ndim).reshape(ndim, -1).T

        # use these to index into np.array([-1, 0, 1]) to get offsets
        offsets = np.arange(-dist, dist + 1, 1, dtype=int).take(offset_idx)

        return offsets

    def debugDot(self, cords):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (cords[0] - 5, cords[1] - 5, 10, 10))

    def get_center_box(self):
        if self.screen_width > self.boxCount[0] * self.boxSize[0]:
            xval = [max(0, (self.topleftBox[0] + self.boxSize[0] *
                            self.boxCount[0]) - self.screen_width), min(0, self.topleftBox[0])]
        else:
            xval = [self.translateX(0) - self.screen_width / 2]
        if self.screen_height > self.boxCount[1] * self.boxSize[1]:
            yval = [max(0, (self.topleftBox[1] + self.boxSize[1] * self.boxCount[1]
                            ) - self.screen_height), min(0, self.topleftBox[1])]
        else:
            yval = [self.translateY(0) - self.screen_height / 2]

        # corners = (max(xval, key=lambda x: abs(x)), max(yval, key=lambda x: abs(x)))
        corners = (sum(xval), sum(yval))

        self.centerCoordinates = ((self.translateX(0) - self.topleftBox[0] - corners[0]) / self.boxSize[0], (
            self.translateY(0) - self.topleftBox[1] - corners[1]) / self.boxSize[1])

        if (self.boxToScreenRatio % 2) == 0:
            centerBox = (int(np.floor(self.centerCoordinates[0]))), int(
                np.floor(self.centerCoordinates[1]))
        else:
            centerBox = (int(np.round(self.centerCoordinates[0])), int(
                np.round(self.centerCoordinates[1])))

        return centerBox

    def plotOrbits(self):
        self.orbitSizePixels = abs(self.size / self.pixelUnit)

        totalSize = (min(self.screen_width, self.orbitSizePixels),
                     min(self.screen_height, self.orbitSizePixels))
        self.boxCount = (int(np.floor(self.orbitSizePixels / (totalSize[0] / self.boxToScreenRatio))), int(
            np.floor(self.orbitSizePixels / (totalSize[1] / self.boxToScreenRatio))))
        self.boxSize = (int(self.orbitSizePixels /
                            self.boxCount[0]), int(self.orbitSizePixels / self.boxCount[1]))

        self.orbits = []
        self.orbitRects = []

        # color = list(np.random.choice(range(256), size=3))
        # color = [(0, 255, 0), (0, 0, 255)]

        for x in range(self.boxCount[0]):
            self.orbits.append([])
            self.orbitRects.append([])
            # color = list(reversed(color))
            for y in range(self.boxCount[1]):
                self.orbits[x].append(pygame.Surface(
                    self.boxSize, pygame.SRCALPHA))
                # self.orbits[x][y].fill(color[(y) % 2])

                # point = (self.topleftBox[0] + x * self.boxSize[0], self.topleftBox[1] + y * self.boxSize[1])
                # self.orbitRects[x].append(self.orbits[x][y].get_rect(topleft=point))
                # oppdaterer posisjon senere om nødvendig
                self.orbitRects[x].append(None)

        if (self.boxToScreenRatio % 2) == 0:
            dist = self.boxToScreenRatio/2
        else:
            dist = int(np.ceil(self.boxToScreenRatio/2))

        size = self.boxToScreenRatio + 1

        self.boxOffsets = self.get_offsets(dist, size)

        for body in self.solar_system.bodies:
            for index in range(1, len(body.posarr[0])):

                # vektor fra univers hjørne til senter til punkt
                p1 = ((self.translateX(body.posarr[0][index - 1]) - self.translateX(0)) + self.orbitSizePixels / 2,
                      (self.translateY(body.posarr[1][index - 1]) - self.translateY(0)) + self.orbitSizePixels / 2)
                p2 = ((self.translateX(body.posarr[0][index]) - self.translateX(0)) + self.orbitSizePixels / 2,
                      (self.translateY(body.posarr[1][index]) - self.translateY(0)) + self.orbitSizePixels / 2)

                p1box = (p1[0] % self.boxSize[0], p1[1] % self.boxSize[1])
                p2box = (-(np.floor(p1[0] / self.boxSize[0]) - np.floor(p2[0] / self.boxSize[0])) * self.boxSize[0] + p2[0] % self.boxSize[0],
                         -(np.floor(p1[1] / self.boxSize[1]) - np.floor(p2[1] / self.boxSize[1])) * self.boxSize[1] + p2[1] % self.boxSize[1])
                pygame.draw.aaline(self.orbits[int(np.floor(p1[0] / self.boxSize[0]))][int(
                    np.floor(p1[1] / self.boxSize[1]))], body.color, p1box, p2box)

    def updateOrbits(self):

        for body in self.solar_system.bodies:
            p1 = ((self.translateX(body.posarr[0][-2]) - self.translateX(0)) + self.orbitSizePixels / 2,
                  (self.translateY(body.posarr[1][-2]) - self.translateY(0)) + self.orbitSizePixels / 2)
            p2 = ((self.translateX(body.posarr[0][-1]) - self.translateX(0)) + self.orbitSizePixels / 2,
                  (self.translateY(body.posarr[1][-1]) - self.translateY(0)) + self.orbitSizePixels / 2)

            # koordinater relativ til boks
            p1box = (p1[0] % self.boxSize[0], p1[1] % self.boxSize[1])
            p2box = (-(np.floor(p1[0] / self.boxSize[0]) - np.floor(p2[0] / self.boxSize[0])) * self.boxSize[0] + p2[0] % self.boxSize[0], -(
                np.floor(p1[1] / self.boxSize[1]) - np.floor(p2[1] / self.boxSize[1])) * self.boxSize[1] + p2[1] % self.boxSize[1])

            pygame.draw.aaline(self.orbits[int(np.floor(p1[0] / self.boxSize[0]))][int(
                np.floor(p1[1] / self.boxSize[1]))], body.color, p1box, p2box)

        self.topleftBox = (self.translateX(
            0) - self.orbitSizePixels / 2, self.translateY(0) - self.orbitSizePixels / 2)

        self.centerBox = self.get_center_box()

        p = self.centerBox
        neighbours = p + self.boxOffsets  # apply offsets to p

        # remove squares outside universe box
        neighbours = neighbours[np.all(neighbours < self.boxCount, axis=1)]
        neighbours = neighbours[np.all(neighbours > (-1, -1), axis=1)]

        for pos in neighbours:
            # oppdaterer kun de nødvendige rect ene
            point = (self.topleftBox[0] + pos[0] * self.boxSize[0],
                     self.topleftBox[1] + pos[1] * self.boxSize[1])
            self.orbitRects[pos[0]][pos[1]] = self.orbits[pos[0]
                                                          ][pos[1]].get_rect(topleft=point)

            # blitter boxene som vil vises på skjermen
            self.screen.blit(
                self.orbits[pos[0]][pos[1]], self.orbitRects[pos[0]][pos[1]])

    def debugChunks(self):
        # color = list(np.random.choice(range(256), size=3))

        # debug square
        universe = pygame.Surface(
            (self.orbitSizePixels, self.orbitSizePixels), pygame.SRCALPHA)
        universe.fill((0, 255, 255, 100))
        universeRect = universe.get_rect(
            center=(self.translateX(0), self.translateY(0)))
        self.screen.blit(universe, universeRect)

        # debug dot
        p = (self.topleftBox[0] + self.centerCoordinates[0] * self.boxSize[0],
             self.topleftBox[1] + self.centerCoordinates[1] * self.boxSize[1])
        self.debugDot(p)
        self.info.append(f"{p}")

        color = [(0, 255, 0), (0, 0, 255)]

        for x in range(self.boxCount[0]):
            color = list(reversed(color))
            for y in range(self.boxCount[1]):
                self.orbits[x][y].fill(color[(y) % 2])

        # print debug square
        # x = np.zeros((self.boxCount[1], self.boxCount[0]), int)
        # x[tuple(neighbours.T)] = 1
        # print(x)
        # print("----------------------------------------------------")

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

    def displayInfo(self):

        self.info.append(
            f"Time passed: {np.round((self.solar_system.framenum * self.solar_system.iterPerFrame) / self.solar_system.timeDivisor, 1)} {self.solar_system.timeUnit}")
        self.info.append(f"box count: {self.boxCount}")
        self.info.append(
            f"memory surface array: { np.round(sys.getsizeof(self.orbits)/(1024), 2)} KB")
        self.info.append(
            f"memory rect array: {np.round(sys.getsizeof(self.orbitRects)/(1024), 2)} KB")

        if self.lockOnTo:
            self.info.append(f"{self.lockOnTo.name}")
            self.info.append(f"Position: {self.lockOnTo.position}")
            self.info.append(f"Velocity: {self.lockOnTo.velocity}")
            self.info.append(f"Radius: {self.lockOnTo.radius}")
            self.info.append(f"Mass: {self.lockOnTo.mass}")

        infoSurface = pygame.Surface(
            (600, self.smallFontSize * len(self.info)), pygame.SRCALPHA)

        for i, j in enumerate(self.info):
            text = self.smallFont.render(j, True, (255, 255, 255))
            textRect = text.get_rect(bottomleft=(
                0, self.smallFontSize + self.smallFontSize * i))
            infoSurface.blit(text, textRect)

        infoRect = infoSurface.get_rect(bottomleft=(0, self.screen_height))
        self.screen.blit(infoSurface, infoRect)

    def lockOn(self):
        self.moveCamera(
            pos=(self.lockOnTo.position[0], self.lockOnTo.position[1]))

    def dragAndDrop(self):
        x, y = pygame.mouse.get_pos()
        self.offsetWidth -= self.pixelUnit * (self.prevX - x)
        self.offsetHeight -= self.pixelUnit * (self.prevY - y)

        # old_surface_saved = self.orbits

        # rect = self.orbits.get_rect(topleft=(-self.offsetWidth * (self.prevY - y), -self.offsetHeight))
        # self.screen.blit(old_surface_saved, rect)
        # del old_surface_saved

        self.prevX = x
        self.prevY = y

    def tag(self, body, pos):
        bodyrect = body.sprite.image.get_rect()

        point = (pos[0] + bodyrect[2] / 4, pos[1] - bodyrect[3]/2 * 0.7)

        tag = pygame.Surface((200, 30), pygame.SRCALPHA)
        text = self.font.render(body.name, True, (255, 255, 255))
        textRect = text.get_rect(bottomleft=point)
        pygame.draw.aaline(tag, body.color, (0, 30), (10, self.fontSize))
        pygame.draw.aaline(tag, body.color, (10, self.fontSize),
                           (textRect[2] + 10, self.fontSize))
        tag.blit(text, (10, 0))

        tagrect = tag.get_rect(bottomleft=point)
        self.screen.blit(tag, tagrect)

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
                    self.zoom(max(self.scale - 15, 5))
                if e.button == 5:
                    self.zoom(min(self.scale + 15, 1000))
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.draging = False
            elif e.type == pygame.VIDEORESIZE:
                self.resizeScreen(e)

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
        self.replotOrbits = True
        self.lastScroll = time()


class planetSprite(pygame.sprite.Sprite):

    imgSize = width, height = 480, 360

    def __init__(self, pygameWindow, body, index):
        super().__init__()
        self.pygameWindow = pygameWindow
        self.body = body

        self.scale(index)
        self.update((0, 0))

    def update(self, pos):
        self.rect = self.image.get_rect(center=pos)
        self.pygameWindow.screen.blit(self.image, self.rect)

    def scale(self, index):
        # må laste bilde på nytt for å hindre rar effekt som kommer av å skalere bildet gjentatte ganger
        self.image = self.pygameWindow.images[index]
        newImgSize = tuple([z * (((self.body.radius + self.pygameWindow.radiusAdder) / self.pygameWindow.pixelUnit) /
                                 self.height) for z in self.imgSize])
        self.image = pygame.transform.scale(self.image, newImgSize)
        self.rect = self.image.get_rect(center=(0, 0))


if __name__ == "__main__":
    import config
    config.main()
