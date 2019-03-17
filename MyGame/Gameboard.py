"""Modulo Game

Modulo principal, responsavel pelas configurações basicas do jogo
"""
import os
from pathlib import Path

import pygame
from pygame.locals import *

from .Map import Mapper
from .Entity import Entity
from .Block import Block

from .Enums.Directions import Direction
from .Enums.BlockTypes import BlockType
from .Enums.EntityTypes import EntityType


class Game():

    def __init__(self, name, icon, size: tuple, tile_size, resources: dict):
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
        self.player = self.selected['entity']
        self.create_screen()
        self.load_resources()
        self.selectDefault(0, 0)

    def create_screen(self):
        """
        Create and customize the window
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, 0, self.tile_size)
        pygame.display.set_caption(self.name)
        self.ico = pygame.image.load(f"./{self.icon}")
        pygame.display.set_icon(self.ico)
        self.clock = pygame.time.Clock()

    def load_resources(self):
        """
        Load the resources of game
        """
        self.gameboard = {
            "screen": self.screen,
            "update": self.update,
            "font": self.resources['font']
        }
        self.fake = Entity(
            name='fake',
            type='fake',
            position=[32,32],
            sprites={},
            gameboard=self.gameboard)
        self.load_entities()
        self.load_tilemaps()
        self.load_maps()

    def load_entities(self):
        """
        Load Entities
        """
        self.entities = []
        self._entities = {}
        for _dir, _dirs, filenames in os.walk(self.resources['entities']):
            for sub_dir in _dirs:
                e_path = os.path.join(_dir, sub_dir)
                e_sprites = [x.stem for x in Path(e_path).glob('*.png')]
                if e_sprites != []:
                    sprites = {}
                    for sprite in e_sprites:
                        sprites[sprite] = (f"{e_path}/{sprite}.png")
                    entity = {
                        'type': _dir.replace('/', '\\').split('\\')[-1],
                        'sprites': sprites
                    }
                    self._entities[sub_dir] = entity
        for name, value in self._entities.items():
            e = Entity(
                name=name,
                type=[e for e in EntityType if e.name == value['type'].upper()][0],
                position=[2*self.tile_size, 2*self.tile_size],
                sprites=value['sprites'],
                gameboard=self.gameboard)
            self.entities.append(e)

    def load_tilemaps(self):
        """
        Load Tilemaps
        """
        res_tilemap = self.resources['tilemaps']
        self.tilemaps = {}
        for _dir, _dirs, filenames in os.walk(res_tilemap):
            tilemap = {}
            for sub_dir in _dirs:
                tilemap_path = os.path.join(_dir, sub_dir)
                blocks = [x.stem for x in Path(tilemap_path).glob('*.png')]
                tilemap['blocks'] = {}
                i = 0
                for block in blocks:
                    bl = Block(
                        name=block.split('_')[0],
                        tile_size=self.tile_size,
                        source=f"{res_tilemap}/{sub_dir}/{block}.png",
                        type=[b for b in BlockType if b.name in block.upper()][0])
                    tilemap['blocks'][i] = bl
                    i += 1
                self.tilemaps[sub_dir] = tilemap

    def load_maps(self):
        """
        Load Maps
        """
        res_map = self.resources['maps']
        self.maps = []
        for _dir, _dirs, filenames in os.walk(res_map):
            for filename in filenames:
                self.maps.append(Mapper(
                    name=filename, 
                    path=res_map, 
                    tile_size=self.tile_size,
                    blocks=self.tilemaps[filename.split("_")[0]]['blocks'], 
                    gameboard=self.gameboard))

    def selectDefault(self, mapp: int, entity: int):
        """
        Select default items
            :param mapp:int: default first map
            :param entity:int: default entity player
        """
        self.selected.update({
            'map': self.maps[mapp],
            'entity': [e for e in self.entities if e.type == EntityType.PLAYER][entity]
        })
        self.player = self.selected['entity']

    def try_move(self, direction):
        """
        check if the next position is not solid
            :param posmat:Position of the entity in the matrix
            :param direction:Direction of attempted walking
        """
        self.fake.position = [
            (self.player.posmat[0]*self.tile_size),
            (self.player.posmat[1]*self.tile_size)]
        self.fake.move(direction)
        x, y = int(self.fake.position[1]/self.tile_size), int(self.fake.position[0]/self.tile_size)
        tilemap = self.tilemaps[self.selected['map'].name.split('_')[0]]
        point = self.selected['map'].map['map'][x][y]
        block = [b for b in tilemap['blocks'].values() if b.type.name == point['type'].upper()][0]
        if block.is_solid:
            return False
        return True

    def update(self):
        """
        Update Screen
        """
        pygame.display.flip()
        self.selected['map'].display()
        self.player.display()

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
                        self.player.move(direction.value)
                    else:
                        self.player.sprite_update(direction.value)
                        
            self.stop()
            self.clock.tick(30)
