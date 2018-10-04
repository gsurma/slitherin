import numpy as np

class Tile():
    empty = " "
    snake = "x"
    fruit = "$"
    wall = "#"

    @staticmethod
    def grayscale(tile):
        if tile == Tile.empty:
            return np.float32(0)#np.uint8(255)
        elif tile == Tile.fruit:
            return np.float32(0.75)#np.uint8(200)
        elif tile == Tile.snake:
            return np.float32(0.25)#np.uint8(75)
        else:
            return np.float32(1.0)#np.uint8(0)