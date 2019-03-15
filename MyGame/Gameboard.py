"""Modulo Game

Modulo principal, responsavel pelas configurações basicas do jogo
"""
import os, time, csv
from pathlib import Path

import pygame
from pygame.locals import *

from .Mapper import Map
from .Entity import Entity
from .Enums.Directions import Direction


class Game():
    
    def __init__(self, name, icon, size: tuple, tile_size, resources:dict):
        """
        Initialize the gameboard to run the game
        :name: Name of game
        :icon: Icon path
        :size:tuple: Window size
        :tile_size: Tile size
        :resources:dict: Resources path
        """
        super(Game, self).__init__()
        self.name = name
        self.icon = icon
        self.size = size
        self.tile_size = tile_size
        self.resources = resources
        self.selected = {
            "entity": None,
            "map": None
        }
        self.create_screen()
        self.load_resources()

    def create_screen(self):
        """
        Create and customize the window
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, 0, self.tile_size)
        pygame.display.set_caption(self.name)
        self.ico = pygame.image.load(f"./{self.icon}")
        pygame.display.set_icon(self.ico)

    def load_resources(self):
        """
        Load the resources of game
        """
        self.gameboard = {
            "screen": self.screen,
            "update": self.update,
            "font": self.resources['font']
        }
        # load entities
        self.entities = []
        self._entities = {}
        for dirname, dirnames, filenames in os.walk(self.resources['entities']):
            for subdirname in dirnames:
                entity_path = os.path.join(dirname, subdirname)
                entity_sides = [x.stem for x in Path(entity_path).glob('*.png')]
                if entity_sides != []:
                    entity = {}
                    sides = {}
                    for side in entity_sides:
                        sides[side] = (f"{entity_path}/{side}.png")
                    entity['type']  = dirname.split('\\')[1]
                    entity['sides'] = sides
                    self._entities[subdirname] = entity
        for e, value in self._entities.items():
            self.entities.append(Entity(e, [2*32, 2*32], value['sides'], self.gameboard))
        # load tilemaps
        self.tilemaps = {}
        for dirname, dirnames, filenames in os.walk(self.resources['tilemaps']):
            tilemap = {}
            for subdirname in dirnames:
                tilemap_path = os.path.join(dirname, subdirname)
                blocks = [x.stem for x in Path(tilemap_path).glob('*.png')]
                tilemap['blocks'] = {}
                i = 0
                for block in blocks:
                    tilemap['blocks'][i] = {
                        'name': block.split('_')[0],
                        'path': (f"{self.resources['tilemaps']}/{subdirname}/{block}.png"),
                        'solid': True if block.split('_')[1] == "solid" else False
                    }
                    i += 1
                self.tilemaps[subdirname] = tilemap
        # load maps
        self.maps = []
        self.matrixs = {}
        for dirname, dirnames, filenames in os.walk(self.resources['maps']):
            for filename in filenames:
                mapx = []
                with open(f"{self.resources['maps']}/{filename}", newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for line in spamreader:
                        mapx.append(line)
                self.matrixs[filename.split('.')[0]] = mapx
        for name, value in self.matrixs.items():
            self.maps.append(Map(name, self.tile_size, value, self.tilemaps[name.split("_")[0]]['blocks'], self.gameboard))

    def selectDefault(self, mapp:int, entity:int):
        """
        select default items
        :param mapp:int: default first map
        :param entity:int: default entity player
        """
        self.selected.update({
            'map': self.maps[mapp],
            'entity': self.entities[entity]
        })

    def try_move(self, direction):
        """
        check if the next position is not solid
        :param posmat:Position of the entity in the matrix
        :param direction:Direction of attempted walking
        """
        e = self.selected['entity']
        fake = Entity('fake', [(e.posmat[0]*self.tile_size), (e.posmat[1]*self.tile_size)], {}, self.gameboard)
        fake.move(direction)
        x = int(fake.position[1]/self.tile_size)
        y = int(fake.position[0]/self.tile_size)
        tilemap = self.tilemaps[self.selected['map'].name.split('_')[0]]
        point = int(self.selected['map'].matrix[x][y])
        if tilemap['blocks'][point]['solid']:
            return False
        return True
                
    def update(self):
        """
        Update Screen
        """
        pygame.display.flip()
        self.selected['map'].display()
        self.selected['entity'].display()

    def stop(self):
        """
        Checks if the window is closed
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    def run(self):
        """
        Run! In-Game
        """
        while True:
            self.update()
            self.press = pygame.key.get_pressed()
            self.press_directions = {
                Direction.UP:    (self.press[K_w] or self.press[K_UP]),
                Direction.DOWN:  (self.press[K_s] or self.press[K_DOWN]),
                Direction.LEFT:  (self.press[K_a] or self.press[K_LEFT]),
                Direction.RIGHT: (self.press[K_d] or self.press[K_RIGHT])
            }
            for direction, pressed in self.press_directions.items():
                if pressed:
                    if self.try_move(direction.value):
                        self.selected['entity'].move(direction.value)
            # stop?
            self.stop()
