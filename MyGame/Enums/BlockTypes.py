"""BlockTypes Enum

Types of blocks that make up a map
"""
from enum import Enum


class BlockType(Enum):
    GRASS = [0, False]
    DIRTY = [1, False]
    SAND  = [3, False]
    WALL  = [4, True]
    TREE  = [2, True]
