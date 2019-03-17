"""Entity

Game entities, Player, Mob, Animals...
"""
import time
import pygame
from pygame.locals import *

from .Font import Font


class Entity():

    def __init__(self, name, type, position: list, sprites: dict, gameboard: dict):
        """
        Create a entity
            :param self: 
            :param name:str: Name of entity
            :param type:EntityTypes: Type of entity
            :param position:list: Initial position
            :param sprites:dict: Images sprites of entity
            :param gameboard:dict: Gameboard data
        """   
        super(Entity, self).__init__()
        self.gameboard = gameboard
        self.name = name
        self.type = type
        self.nametag = Font(
            self.gameboard['font'][0],
            self.gameboard['font'][1],
            self.gameboard['screen'])
        self.spawnpoint = position
        self.position = position
        self.posmat = [3, 3]
        self.sprites_loaded = False
        self.sprites = sprites
        self.sprite = "down_2"
        self.direction = "down"
        self.direction_position = {
            "up": [1, -1],
            "down": [1, 1],
            "left": [0, -1],
            "right": [0, 1],
        }

    def move(self, direction: str):
        """
        Move entity
            :param self: 
            :param direction:str: direction of entity
        """
        self.direction = direction
        for key, value in self.direction_position.items():
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
                time.sleep(0.05/4)
            self.sprite_update(self.direction, (1 if i % 2 == 0 else 2))

    def sprite_update(self, direction, side = 2):
        """
        Sprite Update on screen
            :param direction: direction of entity
            :param side: side of entity
        """
        self.direction = direction
        self.sprite = f'{self.direction}_{side}'

    def load_sprites(self):
        """
        Load sprites games
            :param self: 
        """   
        for i in self.sprites:
            if type(self.sprites[i]) == str:
                self.sprites[i] = pygame.image.load(self.sprites[i])
        self.sprites_loaded = True

    def display(self):
        """
        Display entity on screen
            :param self:
        """
        if not self.sprites_loaded:
            self.load_sprites()
        self.nametag.renderize(self.name, [self.position[0] + (32 - len(self.name)), self.position[1]])
        self.gameboard['screen'].blit(self.sprites[self.sprite], self.position)
