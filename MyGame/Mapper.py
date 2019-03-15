"""Mapper Module

Modulo responsavel por gerar mapas
"""
import pygame
from pygame.locals import *


class Map():
    
    def __init__(self, name, tile_size:int ,matrix:list, blocks:dict, gameboard:dict):
        super(Map, self).__init__()
        self.gameboard = gameboard
        self.name = name
        self.mappoint = matrix
        self.matrix = matrix
        self.blocks = blocks
        self.tile_size = tile_size
        self.load_blocks()
        self.map = self.insert()

    def insert(self):
        for i in range(self.get_map_height()):
            self.matrix[i].insert(0, -1)
            self.matrix[i].append(-1)
        aux = []
        for i in range(self.get_map_width()):
            aux.append(-1)
        self.matrix.append(aux)
        self.matrix.insert(0, aux)
        return self.matrix

    def load_blocks(self):
        self.map_blocks = {}
        for i in self.blocks:
            self.map_blocks[i] = pygame.image.load(self.blocks[i]['path'])

    def display(self):
        for line in range(self.get_map_width()):
            for column in range(self.get_map_height()):
                if self.map[column][line] != -1:
                    self.gameboard['screen'].blit(self.map_blocks[int(self.map[column][line])], [(line * self.tile_size), (column * self.tile_size)])

    def get_map_width(self):
        return len(self.matrix[0])

    def get_map_height(self):
        return len(self.matrix)