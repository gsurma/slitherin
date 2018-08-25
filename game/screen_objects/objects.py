from game.helpers.color import Color


class ScreenObject:

    points = []

    def __init__(self, game, color):
        from game.game import Game
        if isinstance(game, Game):
            self.game = game
            self.color = color
        else:
            raise Exception("Pass valid Game object to the constructor")

    def draw(self, surface):
        for point in self.points:
            self.game.draw_pixel(surface, self.color, point)


class SnakeScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.green)


class WallScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.black)


class FruitScreenObject(ScreenObject):
    def __init__(self, game):
        ScreenObject.__init__(self, game, Color.red)
