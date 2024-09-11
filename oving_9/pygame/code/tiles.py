import pygame
import spritesheet


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.world = spritesheet.spritesheet("./Mario\Tilesets\OverWorld.png")
        # images = self.character.load_strip((0, 0, size, size), count, (0, 0, 0))
        # self.animations["run"].append(images[9])
        size = 16
        self.image = self.world.image_at((0, 0, size, size), (0, 0, 0))
        # self.image = pygame.Surface((size,size))
        # self.image.fill((255, 215, 77))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
