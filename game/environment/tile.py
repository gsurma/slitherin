from enum import Enum
import numpy as np


class Tile(Enum):
    empty = " "
    snake = "x"
    fruit = "$"
    wall = "#"
