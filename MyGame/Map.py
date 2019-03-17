"""Map Module

Modulo responsavel por gerar mapas
"""
import yaml

import pygame
from pygame.locals import *

from .Enums.BlockTypes import BlockType


class Mapper(object):
    
    def __init__(self, name, path, tile_size, blocks, gameboard):
        super(Mapper, self).__init__()
        self.name = name
        self.path = path
        self.tile_size = tile_size
        self.blocks = blocks
        self.gameboard = gameboard
        self.map = self.read()

    def read(self):
        """
            Read Map file
        """
        with open(f"{self.path}/{self.name}") as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as err:
                print(err)
        return False

    def display(self):
        """
            Display Map on screen
        """
        self.width = len([column for column in self.map['map'][0]])
        self.height = len([line for line in self.map['map']])
        for x in range(self.width):
            for y in range(self.height):
                block = [b for b in self.blocks.values() if b.type.name == self.map['map'][y][x]['type'].upper()][0]
                position = [(x * self.tile_size), (y * self.tile_size)]
                self.gameboard['screen'].blit(block.surface, position)
