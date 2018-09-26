import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import OrderedDict
from game.helpers.node import Node
from game.environment.action import Action
from game.helpers.constants import Constants
from game.environment.environment import Environment


class BaseGameModel:

    transposition_table = {}

    def __init__(self, long_name, short_name, abbreviation):
        self.abbreviation = abbreviation
        self.long_name = long_name
        self.short_name = short_name

    def move(self, environment):
        self.starting_node = Node(environment.snake[0])
        self.starting_node.action = environment.snake_action
        self.fruit_node = Node(environment.fruit[0])

    def user_input(self, event):
        pass

    def log_score(self, score):
        path = "scores/" + self.short_name + ".csv"
        if not os.path.exists(path):
            with open(path, "w"):
                pass
        scores_file = open(path, "a")
        with scores_file:
            writer = csv.writer(scores_file)
            writer.writerow([score])
        self._save_png(path, "runs", "scores")

    def stats(self):
        path = "scores/" + self.short_name + ".csv"
        if not os.path.exists(path):
            return "(?, ?, ?)"
        scores_file = open(path, "r")
        scores = []
        with scores_file:
            reader = csv.reader(scores_file)
            for row in reader:
                scores.append(float(row[-1]))
        scores = list(map(lambda x: x, scores))
        minimum = min(scores)
        average = round(sum(scores)/float(len(scores)), 1)
        maximum = max(scores)
        return "("+str(minimum)+"/"+str(average)+"/"+str(maximum)+")"

    def reset(self):
        pass

    def _save_png(self, input_path, x_label, y_label):
        x = []
        y = []
        with open(input_path, "r") as scores:
            reader = csv.reader(scores)
            data = list(reader)
            for i in range(0, len(data)):
                x.append(float(i))
                y.append(float(data[i][0]))

        plt.subplots()
        plt.plot(x, y, label="score per run")

        average_range = len(x)
        plt.plot(x[-average_range:], [np.mean(y[-average_range:])] * len(y[-average_range:]), linestyle="--", label="average")

        plt.title(self.short_name)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.legend(loc="upper left")
        plt.savefig("scores/" + self.short_name + ".png", bbox_inches="tight")
        plt.close()


    def _predict(self, environment, model):
        predictions = []
        actions = [Action.left_neighbor(environment.snake_action), environment.snake_action,
                   Action.right_neighbor(environment.snake_action)]
        for action in actions:
            observation_for_prediction = environment.observation(action)
            predictions.append(
                model.model.predict(np.array(observation_for_prediction).reshape(-1, Constants.MODEL_FEATURE_COUNT, 1))
            )
        best_prediction_index = np.argmax(np.array(predictions))
        return actions[best_prediction_index]

    def prepare_training_environment(self, horizontal_pixels=Constants.ENV_WIDTH, vertical_pixels=Constants.ENV_HEIGHT):
        environment = Environment(width=horizontal_pixels,
                           height=vertical_pixels)
        environment.set_wall()
        environment.set_fruit()
        environment.set_snake()
        return environment

    def _path_move_from_transposition_table(self, starting_node, fruit_node):
        path_from_transposition_table = self._path_from_transposition_table(fruit_node)
        if path_from_transposition_table:
            for index in range(0, len(path_from_transposition_table)):
                node = path_from_transposition_table[index]
                if node.point == starting_node.point:
                    destination_node = path_from_transposition_table[index - 1]
                    return destination_node.action
        self.transposition_table = {}
        return None

    def _path_from_transposition_table(self, key):
        try:
            return self.transposition_table[key]
        except KeyError:
            self.transposition_table = {}
            return []

    def _recreate_path_for_node(self, node):
        nodes = [node]
        previous_node = node.previous_node
        while previous_node:
            nodes.append(previous_node)
            previous_node = previous_node.previous_node
        return nodes

    def _best_action_for_runs(self, runs):
        scores_for_actions = {}
        for run in runs:
            if run.action in scores_for_actions.keys():
                scores_for_action = scores_for_actions[run.action]
                scores_for_action.append(run.score)
                scores_for_actions[run.action] = scores_for_action
            else:
                scores_for_actions[run.action] = [run.score]

        average_scores_for_actions = {}
        for action in scores_for_actions.keys():
            average_score_for_action = sum(scores_for_actions[action]) / float(len(scores_for_actions[action]))
            average_scores_for_actions[action] = average_score_for_action
        sorted_average_scores_for_actions = OrderedDict(sorted(average_scores_for_actions.items(), key=lambda t: t[1]))
        return sorted_average_scores_for_actions.keys()[-1]
