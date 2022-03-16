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

        universeSizeWidth = max(2 * self.size, self.screen_width * self.maxPixelUnit) / self.pixelUnit
        universeSizeHeight = max(2 * self.size, self.screen_height * self.maxPixelUnit) / self.pixelUnit

        self.orbits = pygame.Surface((universeSizeWidth, universeSizeHeight), pygame.SRCALPHA)
        self.orbitSizePixels = abs(self.size / self.pixelUnit)

        self.fontSize = 20
        self.font = pygame.font.Font('freesansbold.ttf', self.fontSize)

    def init_objects(self, body, index):
        body.sprite = planetSprite(self, body, index)
        self.sprites.append(body.sprite)
        body.posarr = [[], []]  # lagrer bare 2d
        # lagrer en verdi fra start for å hindre bane tegnigen i å krasje
        body.posarr[0].append(body.position[0])
        body.posarr[1].append(body.position[1])

    def resizeScreen(self, e):
        old_surface_saved = self.screen
        self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
        self.screen_width = e.w
        self.screen_height = e.h
        self.screen.blit(old_surface_saved, (0, 0))
        del old_surface_saved

    def pauseSim(self):
        self.solar_system.paused = not self.solar_system.paused

    def plotOrbits(self):

        self.orbitSizePixels = abs(self.size / self.pixelUnit)
        self.orbits = pygame.Surface((self.orbitSizePixels, self.orbitSizePixels), pygame.SRCALPHA)


        for body in self.solar_system.bodies:
            for index in range(1, len(body.posarr[0])):

                p1 = ((self.translateX(body.posarr[0][index - 1]) - self.translateX(0)) + self.orbitSizePixels / 2, (self.translateY(body.posarr[1][index - 1]) - self.translateY(0)) + self.orbitSizePixels / 2)
                p2 = ((self.translateX(body.posarr[0][index]) - self.translateX(0)) + self.orbitSizePixels / 2, (self.translateY(body.posarr[1][index]) - self.translateY(0)) + self.orbitSizePixels / 2)

                pygame.draw.aaline(self.orbits, body.color, p1, p2)

        rect = self.orbits.get_rect(
            center=(self.translateX(0), self.translateY(0)))
        self.screen.blit(self.orbits, rect)

    def updateOrbits(self):

        for body in self.solar_system.bodies:
            body.posarr[0].append(body.position[0])
            body.posarr[1].append(body.position[1])

            p1 = ((self.translateX(body.posarr[0][-2]) - self.translateX(0)) + self.orbitSizePixels / 2,
                  (self.translateY(body.posarr[1][-2]) - self.translateY(0)) + self.orbitSizePixels / 2)
            p2 = ((self.translateX(body.posarr[0][-1]) - self.translateX(0)) + self.orbitSizePixels / 2,
                  (self.translateY(body.posarr[1][-1]) - self.translateY(0)) + self.orbitSizePixels / 2)

            pygame.draw.aaline(self.orbits, body.color, p1, p2)

        rect = self.orbits.get_rect(center=(self.translateX(0), self.translateY(0)))
        self.screen.blit(self.orbits, rect)

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
        unviverseSizeWidth = max( 2 * self.size, self.screen_width * self.maxPixelUnit)
        unviverseSizeHeight = max( 2 * self.size, self.screen_height * self.maxPixelUnit)

        # nedre grense må kompansere for at skjermposisjonen er definert som øverste venstre hjørne
        self.offsetWidth = max(- unviverseSizeWidth + self.screen_width * self.pixelUnit, min(self.offsetWidth, unviverseSizeWidth))
        self.offsetHeight = max(- unviverseSizeHeight + self.screen_height * self.pixelUnit, min(self.offsetHeight, unviverseSizeHeight))

    def lockOn(self):
        self.moveCamera( pos=(self.lockOnTo.position[0], self.lockOnTo.position[1]))

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
        pygame.draw.aaline(tag, body.color, (10, self.fontSize), (textRect[2] + 10, self.fontSize))
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
                    self.zoom(max(self.scale - 15, 1))
                if e.button == 5:
                    self.zoom(min(self.scale + 15, 1000))
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.draging = False
            elif e.type == pygame.VIDEORESIZE:
                self.resizeScreen(e)

    def translateX(self, x): return (x + self.offsetWidth) / self.pixelUnit

    def translateY(self, y): return (y + self.offsetHeight) / self.pixelUnit

    def updatePygame(self, framenum):
        self.screen.fill((0, 0, 0))
        self.eventChecker()
        self.moveCamera()
        self.updateOrbits()

        if self.lockOnTo:
            self.lockOn()
        elif self.draging:
            self.dragAndDrop()

        for int, body in enumerate(self.solar_system.bodies):
            x = self.translateX(body.position[0])
            y = self.translateY(body.position[1])
            body.sprite.update(((x, y)))
            self.tag(body, (x, y))

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
        self.plotOrbits()


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
    print("call")

    config.main()
