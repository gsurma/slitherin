
import random
import math
import numpy as np
from collections import deque
from game.helpers.point import Point
from game.environment.action import Action
from game.environment.tile import Tile
from game.helpers.constants import Constants


class Environment:

    snake = []
    fruit = []
    wall = []

    snake_moves = 0
    snake_length = 1
    snake_action = None

    def __init__(self, width=Constants.ENV_WIDTH, height=Constants.ENV_HEIGHT):
        self.width = width
        self.height = height
        self.tiles = []
        self.frames = []
        for y in range(0, self.height):
            self.tiles.append([])
            for x in range(0, self.width):
                self.tiles[y].append(Tile.empty)

    def full_step(self, action):
        terminal = not self.step(action)
        reward = 1 if self.eat_fruit_if_possible() else 0
        if terminal:
            reward = -1
        state = self.state()
        return state, reward, terminal

    def step(self, action):
        if Action.is_reverse(self.snake_action, action):
            #print "Forbidden reverse action attempt!"
            return
        self.snake_action = action
        head = self.snake[0]
        x, y = self.snake_action
        new = Point(x=(head.x + x),
                    y=(head.y + y))
        if new in self.snake:
            #print "Hit snake"
            return False
        elif new in self.wall:
            #print "Hit wall"
            return False
        else:
            self.snake_moves += 1
            self.snake.insert(0, new)
            self.tiles[new.y][new.x] = Tile.snake
            if len(self.snake) > self.reward():
                last = self.snake.pop()
                self.tiles[last.y][last.x] = Tile.empty
            self._update_frames()
            return True

    def state(self):
        return np.asarray(self._frames())

    def reward(self):
        return self.snake_length

    def distance_from_fruit(self):
        head = self.snake[0]
        fruit = self.fruit[0]
        x_distance = head.x - fruit.x
        y_distance = head.y - fruit.y
        return math.hypot(x_distance, y_distance)

    def observation(self, new_action):
        head = self.snake[0]
        left_neighbor_action = Action.left_neighbor(self.snake_action)
        left_neighbor_point = Point(head.x+left_neighbor_action[0], head.y+left_neighbor_action[1])
        left_neighbor_accessible = self._is_point_accessible(left_neighbor_point)
        top_neighbor_point = Point(head.x + self.snake_action[0], head.y + self.snake_action[1])
        top_neighbor_accessible = self._is_point_accessible(top_neighbor_point)
        right_neighbor_action = Action.right_neighbor(self.snake_action)
        right_neighbor_point = Point(head.x+right_neighbor_action[0], head.y+right_neighbor_action[1])
        right_point_accessible = self._is_point_accessible(right_neighbor_point)
        action_vector = Action.vector(self.snake_action, new_action)
        return [action_vector, left_neighbor_accessible, top_neighbor_accessible, right_point_accessible, self._angle_from_fruit()]

    def possible_actions_for_current_action(self, current_action):
        actions = Action.all()
        reverse_action = (current_action[0] * -1, current_action[1] * -1)
        actions.remove(reverse_action)
        return actions

    def eat_fruit_if_possible(self):
        if self.fruit[0] == self.snake[0]:
            self.snake_length += 1
            self.snake_moves = 0
            if self._is_winning():
                return True
            self.set_fruit()
            return True
        return False

    def set_wall(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    self.tiles[y][x] = Tile.wall
        self.wall = self._points_of(Tile.wall)
        return self.wall

    def set_fruit(self):
        self._clear_environment_for(Tile.fruit)
        random_position = self._random_available_position()
        self.tiles[random_position.x][random_position.y] = Tile.fruit
        self.fruit = self._points_of(Tile.fruit)
        return self.fruit

    def set_snake(self):
        self._clear_environment_for(Tile.snake)
        random_position = self._random_available_position()
        self.tiles[random_position.x][random_position.y] = Tile.snake
        self.snake = self._points_of(Tile.snake)
        self.snake_length = 1
        self.snake_moves = 0
        if self.snake_action is None:
            self.snake_action = random.choice(Action.all())
        return self.snake

    def print_path(self, path):
        environment_string = ""
        for y in range(0, self.height):
            environment_string += "\n"
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                for p in path:
                    if tile == Tile.empty and p.point == Point(x, y):
                        tile = Action.description(p.action)
                environment_string += " " + tile + " "
        print environment_string

    def print_to_console(self):
        environment_string = ""
        for y in range(0, self.height):
            environment_string += "\n"
            for x in range(0, self.width):
                environment_string += " " + self.tiles[y][x] + " "
        print environment_string

    def _frame(self):
        grayscale = [[Tile.grayscale(tile) for tile in row] for row in self.tiles]
        return np.array(grayscale)

    def _frames(self):
        while len(self.frames) < Constants.FRAMES_TO_REMEMBER:
            self.frames.append(self._frame())
        return self.frames

    def _update_frames(self):
        self.frames.append(self._frame())
        while len(self.frames) > Constants.FRAMES_TO_REMEMBER:
            self.frames.pop(0)

    def is_in_fruitless_cycle(self):
        return self.snake_moves >= self._available_tiles_count()

    def _angle_from_fruit(self):
        snake = self.snake[0]
        fruit = self.fruit[0]
        angle = math.atan2(fruit.y - snake.y, fruit.x - snake.x)
        adjusted_angles = Action.adjusted_angles(self.snake_action)
        adjusted_angle_cw = angle + adjusted_angles[0]
        adjusted_angle_ccw = angle - adjusted_angles[1]
        if abs(adjusted_angle_cw) < abs(adjusted_angle_ccw):
            return adjusted_angle_cw
        else:
            return adjusted_angle_ccw

    def _is_point_accessible(self, point):
        return int(self.tiles[point.y][point.x] == Tile.empty
                   or self.tiles[point.y][point.x] == Tile.fruit)

    def _points_of(self, environment_object):
        points = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                if tile == environment_object:
                    points.append(Point(x, y))
        return points

    def _clear_environment_for(self, environment_object):
        points_to_clear = self._points_of(environment_object)
        for point in points_to_clear:
            self.tiles[point.y][point.x] = Tile.empty

    def _random_available_position(self):
        tile = None
        while tile is None or tile is not Tile.empty:
            random_x = random.randint(0, self.height-1)
            random_y = random.randint(0, self.width-1)
            tile = self.tiles[random_x][random_y]
        return Point(random_x, random_y)

    def _available_tiles_count(self):
        return (self.width-2) * (self.height-2)

    def _is_winning(self):
        return self.reward() == self._available_tiles_count()

