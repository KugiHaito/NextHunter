"""Items Enum

Items of game
"""
from enum import Enum


class Items(Enum):
    # TypeName : index, dragable, catchable
    KEY = [0, False, True]
    BOX = [1, True, False]
    FOOD = [2, False, True]