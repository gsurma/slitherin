
from game.helpers.point import Point
from game.environment.tile import Tile
from game.helpers.node import Node
from game.environment.action import Action
from game.models.base_game_model import BaseGameModel
from game.models.domain_specific.shortest_path_bfs_ai_solver import ShortestPathBFSSolver


class LongestPathSolver(BaseGameModel):

    def __init__(self):
        BaseGameModel.__init__(self, "Longest Path", "longest_path", "lp")

    def move(self, environment):
        BaseGameModel.move(self, environment)

        longest_path = self.longest_path(self.starting_node, self.fruit_node, environment)

        for index in range(0, len(longest_path)):
            node = longest_path[index]
            if node == self.starting_node:
                return longest_path[index+1].action
        return environment.snake_action

    def longest_path(self, start, end, environment):
        longest_path_from_transposition_table = self._path_from_transposition_table(end)
        if longest_path_from_transposition_table:
            return longest_path_from_transposition_table
        shortest_path_solver = ShortestPathBFSSolver()
        path = shortest_path_solver.shortest_path(environment, start, end)
        path.reverse()

        if not path or len(path) <= 1:
            return []
        index = 0
        while True:
            a = path[index]
            b = path[index+1]

            extended_nodes = []

            rotated_actions = [Action.left_neighbor(b.action), Action.right_neighbor(b.action)]
            for rotated_action in rotated_actions:
                inverse_a_action = (a.action[0] * -1, a.action[1] * -1)
                if rotated_action == inverse_a_action:
                    continue
                rotated_neighbor = self._neighbor(a, rotated_action, environment)
                if rotated_neighbor:
                    directed_neighbor = self._neighbor(rotated_neighbor, b.action, environment)
                    if directed_neighbor:
                        if rotated_neighbor not in path and directed_neighbor not in path:
                            extended_nodes = [rotated_neighbor, directed_neighbor]

            if len(extended_nodes) == 2:
                x = extended_nodes[0]
                y = extended_nodes[1]

                path.insert(index+1, x)
                path.insert(index+2, y)

                b = path[index+3]
                b.action = (b.point.x - y.point.x, b.point.y - y.point.y)
                path[index+3] = b
                continue

            index += 1
            if index == len(path)-1:
                break
        self.transposition_table[end] = path
        return path

    def _neighbor(self, node, action, environment):
        neighbor_point = Point(node.point.x + action[0],
                               node.point.y + action[1])
        neighbor_tile = environment.tiles[neighbor_point.y][neighbor_point.x]
        if neighbor_tile == Tile.empty or neighbor_tile == Tile.fruit:
            neighbor_node = Node(neighbor_point)
            neighbor_node.previous_node = node
            neighbor_node.action = action
            return neighbor_node
        return None
