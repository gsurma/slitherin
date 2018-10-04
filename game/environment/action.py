#!/usr/bin/env python
# -*- coding: utf-8 -*

import math


class Action():
    left = (-1, 0)
    up = (0, -1)
    right = (1, 0)
    down = (0, 1)

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    @staticmethod
    def description(action):
        if action == Action.up:
            return "↑"
        elif action == Action.down:
            return "↓"
        elif action == Action.left:
            return "←"
        else:
            return "→"

    @staticmethod
    def is_reverse(current_action, new_action):
        inverse_action = (current_action[0] * -1, current_action[1] * -1)
        return new_action == inverse_action

    @staticmethod
    def action_from_vector(vector):
        return Action.possible()[vector]

    @staticmethod # So that turning left is -1, forward is 0 and turning right is 1
    def vector(start, end):
        start_index = Action.all().index(start)
        end_index = Action.all().index(end)
        diff = end_index-start_index
        bounded = max(min(diff, 1), -1)
        if abs(diff) > 1:
            return -bounded
        return bounded

    @staticmethod
    def left_neighbor(action):
        actions = Action.all()
        actions.reverse()
        return Action._neighbor(action, actions)

    @staticmethod
    def right_neighbor(action):
        actions = Action.all()
        return Action._neighbor(action, actions)

    @staticmethod
    def _neighbor(action, actions):
        actions_count = len(actions)
        for i in range(0, actions_count):
            if actions[i] == action:
                if i == actions_count-1:
                    return actions[0]
                else:
                    return actions[i+1]

    @staticmethod
    def adjusted_angles(action):
        if action == Action.up:
            return math.pi / 2, math.pi * 3 / 2
        elif action == Action.left:
            return math.pi, math.pi
        elif action == Action.down:
            return math.pi * 3 / 2, math.pi / 2
        else:
            return 0, 0 # Angle is by default calculated according to the Action.right

    @staticmethod
    def normalized_action(current_action, new_action):
        if new_action == Action.left:
            return Action.left_neighbor(current_action)
        elif new_action == Action.right:
            return Action.right_neighbor(current_action)
        else:
            return current_action

    @staticmethod
    def possible():
        return [Action.left, Action.up, Action.right]

    @staticmethod
    def all():
        return [Action.left, Action.up, Action.right, Action.down]