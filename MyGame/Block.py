"""Block Class

Block, a part of map
"""
import pygame
from pygame.sprite import Sprite

from .Enums.BlockTypes import BlockType


class Block(pygame.sprite.Sprite):
    def __init__(self, name, data, type: BlockType, pos: list, size: int, spawnpoint: bool = False):
        super(Block, self).__init__()
        self.name = name
        self.type = type
        self.size = size
        # self.data = data
        # self.image = pygame.image.load(self.data, self.name)
        self.image = data
        self.spawnpoint = spawnpoint
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (pos[0]*self.size), (pos[1]*self.size)

    @property
    def pos(self):
        return [self.rect.x, self.rect.y]

    @pos.setter
    def pos(self, value):
        self.rect.x = (value[0]*self.size)
        self.rect.y = (value[1]*self.size)

    @property
    def is_solid(self):
        return self.type.value[1]

    @property
    def is_dragable(self):
        return self.type.value[2]

    @property
    def is_catchable(self):
        return self.type.value[3]
