
import random
import copy
import numpy as np
from statistics import mean
from game.models.base_game_model import BaseGameModel
from tf_models.dnn_model import DeepNeuralNetModel
from game.helpers.constants import Constants


class BaseDNNGameModel(BaseGameModel):

    model = None

    def __init__(self, long_name, short_name, abbreviation):
        BaseGameModel.__init__(self, long_name, short_name, abbreviation)

    def move(self, environment):
        if self.model is None:
            self.model = DeepNeuralNetModel(Constants.MODEL_DIRECTORY + "dnn/")
        BaseGameModel.move(self, environment)


class DNNSolver(BaseDNNGameModel):

    def __init__(self):
        BaseDNNGameModel.__init__(self, "Deep Neural Net", "deep_neural_net", "dnn")

    def move(self, environment):
        BaseDNNGameModel.move(self, environment)
        predicted_action = self._predict(environment, self.model)
        return predicted_action


class DNNTrainer(BaseDNNGameModel):

    def __init__(self):
        BaseDNNGameModel.__init__(self, "Deep Neural Net", "deep_neural_net_trainer", "dnnt")

    def move(self, environment):
        BaseDNNGameModel.move(self, environment)
        print ""
        print self.long_name + ": train and test"
        print ""
        while True:
            self._train(100)
            self._test(100)

    def _train(self, training_runs):
        training_data = np.array(self._training_observations(training_runs))
        x = np.array([i[0] for i in training_data]).reshape(-1, Constants.MODEL_FEATURE_COUNT, 1)
        y = np.array([i[1] for i in training_data]).reshape(-1, 1)
        self.model.model.fit(x, y)
        self.model.save()

    def _test(self, testing_runs):
        moves_per_run = []
        eat_fruit_moves = 0
        good_moves = 0
        bad_moves = 0
        death_moves = 0

        for i in range(0, testing_runs):
            environment = self.prepare_training_environment(10, 10)
            while True:
                predicted_action = self._predict(environment, self.model)
                pre_distance_from_fruit = environment.distance_from_fruit()
                pre_length = environment.reward()
                if not environment.step(predicted_action) or environment.is_in_fruitless_cycle():
                    death_moves += 1
                    break
                environment.eat_fruit_if_possible()
                post_distance_from_fruit = environment.distance_from_fruit()
                post_length = environment.reward()
                if post_length > pre_length:
                    eat_fruit_moves += 1
                elif post_distance_from_fruit < pre_distance_from_fruit:
                    good_moves += 1
                else:
                    bad_moves += 1
            moves_per_run.append(environment.reward())
        mean_score = mean(moves_per_run)
        print "Mean score: " + str(mean_score)
        print "Eat fruit moves: " + str(eat_fruit_moves)
        print "Good moves: " + str(good_moves)
        print "Bad moves: " + str(bad_moves)
        print "Death moves: " + str(death_moves)

    def _training_observations(self, training_runs):
        new_environment = self.prepare_training_environment(10, 10)
        observations = []
        for run_index in range(0, training_runs):
            environment = copy.deepcopy(new_environment)
            observations_for_run = []
            while True:
                random_action = random.choice(environment.possible_actions_for_current_action(environment.snake_action))
                environment_observation = environment.observation(random_action)
                pre_distance_from_fruit = environment.distance_from_fruit()
                pre_length = environment.reward()
                alive = environment.step(random_action)
                if not alive:
                    break
                environment.eat_fruit_if_possible()
                post_distance_from_fruit = environment.distance_from_fruit()
                post_length = environment.reward()

                if post_length > pre_length:
                    observation = [environment_observation, [0.7]]
                elif post_distance_from_fruit < pre_distance_from_fruit:
                    observation = [environment_observation, [0.1]]
                else:
                    observation = [environment_observation, [-0.2]]
                observations_for_run.append(observation)
            observation = [environment_observation, [-1.0]]
            observations_for_run.append(observation)
            observations += observations_for_run
        return observations

