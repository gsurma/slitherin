import pygame
import sys
from screen_objects.objects import SnakeScreenObject, FruitScreenObject, WallScreenObject
from pygame.locals import *
from helpers.point import Point
from helpers.color import Color
from helpers.constants import Constants
from environment.environment import Environment


class Game:

    pygame.init()
    pygame.display.set_caption(Constants.SLITHERIN_NAME)
    icon = pygame.image.load(Constants.ICON_PATH)
    pygame.display.set_icon(icon)
    screen_objects = []
    model = None
    stats = ""

    def __init__(self, game_model, fps, pixel_size, screen_width, screen_height, navigation_bar_height):
        self.model = game_model

        self.stats = self.model.stats()
        self.fps = fps
        self.pixel_size = pixel_size
        self.navigation_bar_height = navigation_bar_height
        self.screen = pygame.display.set_mode((screen_width, screen_height), 0, Constants.SCREEN_DEPTH)
        self.surface = pygame.Surface(self.screen.get_size())
        self.horizontal_pixels = screen_width / pixel_size
        self.vertical_pixels = (screen_height-navigation_bar_height) / pixel_size

        self.environment = Environment(width=self.horizontal_pixels,
                                       height=self.vertical_pixels)

        self.wall = WallScreenObject(self)
        self.wall.points = list(map(lambda x: self._screen_normalized_point(x), self.environment.set_wall()))
        self.screen_objects.append(self.wall)

        self.fruit = FruitScreenObject(self)
        self.fruit.points = list(map(lambda x: self._screen_normalized_point(x), self.environment.set_fruit()))
        self.screen_objects.append(self.fruit)

        self.snake = SnakeScreenObject(self)
        self.snake.points = list(map(lambda x: self._screen_normalized_point(x), self.environment.set_snake()))
        self.screen_objects.append(self.snake)

        while True:
            self._handle_user_input()
            pygame.time.Clock().tick(fps)
            self.environment.eat_fruit_if_possible()
            ai_action = self.model.move(self.environment)
            if not self.environment.step(ai_action):
                self.model.reset()
                self.model.log_score(self.environment.reward())
                self.stats = self.model.stats()
                self.environment.set_snake()
            self._sync_screen_with_environment()
            self._draw_screen()
            self._display()

    def draw_pixel(self, surf, color, point):
        rect = pygame.Rect((point.x, point.y), (self.pixel_size, self.pixel_size))
        pygame.draw.rect(surf, color, rect)

    def _draw_screen(self):
        self.surface.fill(Color.white)
        for game_object in self.screen_objects:
            game_object.draw(self.surface)
        for x in range(0, (self.horizontal_pixels*self.pixel_size)+1):
            self.draw_pixel(self.surface, Color.gray, Point(x, 0))
            for y in range(0, (self.navigation_bar_height-self.pixel_size)+1):
                self.draw_pixel(self.surface, Color.gray, Point(x, y))

        font = pygame.font.SysFont(Constants.FONT, int(self.navigation_bar_height / 1.3))
        score_text = font.render(str(self.environment.reward()), 1, Color.green)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (self.navigation_bar_height/2, self.navigation_bar_height/2)
        self.surface.blit(score_text, score_text_rect)

        solver_text = font.render(self.model.long_name + " " + self.stats, 1, Color.black)
        solver_text_rect = solver_text.get_rect()
        solver_text_rect.center = (self.screen.get_rect().width/2, self.navigation_bar_height/2)
        self.surface.blit(solver_text, solver_text_rect)
        self.screen.blit(self.surface, (0, 0))

    def _sync_screen_with_environment(self):
        self.fruit.points = list(map(lambda x: self._screen_normalized_point(x), self.environment.fruit))
        self.snake.points = list(map(lambda x: self._screen_normalized_point(x), self.environment.snake))

    def _display(self):
        pygame.display.flip()
        pygame.display.update()

    def _screen_normalized_point(self, point):
        return Point(point.x * self.pixel_size, self.navigation_bar_height + (point.y * self.pixel_size))

    def _handle_user_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                self.model.user_input(event)
