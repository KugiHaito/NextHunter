"""Modulo Game

Modulo principal, responsavel pelas configurações basicas do jogo
"""
import os
import io
from zipfile import ZipFile
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
        self.texturepack = 'default'
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
        self.load_texture()

    def load_texture(self):
        """
        Load texture, pack of images, songs, etc...
        """
        self.texture = {}
        with ZipFile(f'{self.resources}/{self.texturepack}.zip', 'r') as texture:
            for item in [i for i in texture.namelist() if not 'README' in i]:
                items, is_dir = item.split('/'), texture.getinfo(item).is_dir()
                if not is_dir:
                    if len(items) == 4:pack, group, entity, sprite = items;self.texture[pack][group][entity].append(sprite)
                    if len(items) == 2:pack, i = items;self.texture[pack].append(i if pack == 'blocks' else pygame.font.Font(io.BytesIO(texture.read(item)), 12))
                else:
                    if len(items) == 2:pack, _ = items;self.texture[pack] = [] if pack in ['blocks', 'HUD'] else {}
                    if len(items) == 3:pack, group, _ = items;self.texture[pack].update({group: {}})
                    if len(items) == 4:pack, group, entity, _ = items;self.texture[pack][group].update({entity: []})

            # TODO: make something for not need ``self.gameboard``
            self.gameboard = {
                "screen": self.screen,
                "update": self.update,
                "font": self.texture['HUD']
            }
            self.fake = Entity(
            name='fake',
            type='fake',
            position=[32,32],
            sprites={},
            gameboard=self.gameboard)

            self.blocks = []
            for block in self.texture['blocks']:
                self.blocks.append({
                    'name': block.split('.')[0],
                    'path': f'blocks/{block}',
                    'type': [b for b in BlockType if b.name in block.upper()][0],
                    'data': pygame.image.load(io.BytesIO(texture.read(f'blocks/{block}'))) })
            self.entities = []

            res_map, self.maps = 'resources/maps/', []
            for _dir, _dirs, filenames in os.walk(res_map):
                for filename in filenames:
                    self.maps.append(Mapper(
                        name=filename, 
                        path=res_map, 
                        tile_size=self.tile_size,
                        blocks=self.blocks,
                        gameboard=self.gameboard))

            for group, entities in self.texture['entities'].items():
                for entity, sprites in entities.items():
                    self.entities.append(Entity(
                        name=entity,
                        type=[e for e in EntityType if e.name == group.upper()][0],
                        # TODO: Set Map spawnpoint to entity (Player)
                        position=[2*self.tile_size, 2*self.tile_size],
                        sprites=[{
                            'name': sprite.split('.')[0],
                            'data': io.BytesIO(texture.read(f'entities/{group}/{entity}/{sprite}'))} for sprite in sprites],
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
        point = self.selected['map'].map[x][y]
        # TODO: Optimize listing of blocks
        block = [b for b in self.selected['map'].blocks.sprites() if b.type.name == point['type'].upper()][0]
        if block.is_solid:
            return False
        return True

    def update(self):
        """
        Update Screen
        """
        pygame.display.flip()
        self.selected['map'].display()
        # TODO: Insert Entities in a pygame.sprite.Group(), for display them with draw() method
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
            self.update()
            self.clock.tick(30)
