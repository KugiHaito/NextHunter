"""Modulo Entidades

Classe representativa de cada entidade
"""
import os, time
import pygame
from pygame.locals import *

from .Font import Font


class Entity():

    def __init__(self, name, pos:list, sides:dict, gameboard:dict):
        super(Entity, self).__init__()
        self.gameboard = gameboard
        self.name = name
        self.nametag = Font(self.gameboard['font'][0], self.gameboard['font'][1], self.gameboard['screen'])
        self.spawnpoint = pos
        self.position = pos
        self.posmat = [3, 3]
        self.sprites_loaded = False
        self.sides = sides
        self.side = "down_2"
        self.direction = "down"
        self.direction_pos = {
            "up": [1, -1],
            "down": [1, 1],
            "left": [0, -1],
            "right": [0, 1],
        }

    def move(self, direction):
        self.direction = direction
        for key, value in self.direction_pos.items():
            if direction == key:
                self.posmat[value[0]] += value[1]
        for i in range(4):
            self.gameboard['update']()
            if self.direction == "left":
                self.position[0] -= 8
            if self.direction == "right":
                self.position[0] += 8
            if self.direction == "down":
                self.position[1] += 8
            if self.direction == "up":
                self.position[1] -= 8
            if self.name != 'fake':
                time.sleep(0.035)
            self.side = f'{self.direction}_{1 if i % 2 == 0 else 2}'
                
    def load_sides(self):
        for i in self.sides:
            if type(self.sides[i]) == str:
                self.sides[i] = pygame.image.load(self.sides[i])
        self.sprites_loaded = True

    def display(self):
        if not self.sprites_loaded:
            self.load_sides()
        x = self.position[0]-(len(self.name)//2 - 30)
        y = self.position[1]
        self.nametag.renderize(self.name, [x, y])
        self.gameboard['screen'].blit(self.sides[self.side], self.position)
    