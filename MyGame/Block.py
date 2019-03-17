"""Block Class

Block, a part of map
"""
import pygame
from .Enums.BlockTypes import BlockType


class Block(object):

    def __init__(self, name, tile_size: int, source, type: BlockType):
        super(Block, self).__init__()
        self.name = name
        self.tile_size = tile_size
        self.source = source
        self.type = type
        self.is_solid = type.value[1]
        self.set_block()

    def set_block(self):
        """
            load a block
        """
        self.surface = pygame.image.load(self.source, self.name)
