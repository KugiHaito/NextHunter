"""Map Module

Modulo responsavel por gerar mapas
"""
import yaml

import pygame
from pygame.locals import *

from .Block import Block
from .Enums.BlockTypes import BlockType


class Mapper(object):
    
    def __init__(self, name, path, tile_size, blocks, gameboard):
        super(Mapper, self).__init__()
        self.name = name
        self.path = path
        self.tile_size = tile_size
        self._blocks = blocks
        self.blocks = pygame.sprite.Group()
        self.gameboard = gameboard
        self.map = self.read()['map']
        self.width = len([column for column in self.map[0]])
        self.height = len([line for line in self.map])
        self.load_blocks()

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

    def load_blocks(self):
        """
        Load blocks of map
        """
        for x in range(self.width):
            for y in range(self.height):
                block = [b for b in self._blocks if self.map[y][x]['type'].upper() == b['type'].name][0]
                self.blocks.add(
                    Block(
                        block['name'], block['data'],
                        block['type'], [x, y],
                        self.tile_size,
                        True if self.map[y][x].get('spawnpoint') else False ))
        return self.blocks


    def display(self):
        """
        Display Map on screen
        """
        self.blocks.update()
        self.blocks.draw(self.gameboard['screen'])
