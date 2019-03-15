"""Directions Enum

List of directions, utilitary for others class
"""
from enum import Enum


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    DOWN = "down"
    UP = "up"