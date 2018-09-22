from game.models.base_game_model import BaseGameModel
from tf_models.dqn_model import DeepQNetModel
from game.helpers.constants import Constants
from game.environment.action import Action
import random
import collections
import numpy as np
import time
import math
from statistics import mean


class BaseDQNGameModel(BaseGameModel):

    model_dir_path = Constants.MODEL_DIRECTORY + "dqn/"
    model_file_name = model_dir_path + Constants.DQN_MODEL_NAME


    def __init__(self, long_name, short_name, abbreviation):
        BaseGameModel.__init__(self, long_name, short_name, abbreviation)
        #self.model = DeepQNetModel.model(self.model_file_name)

    def move(self, environment):
        BaseGameModel.move(self, environment)


class DQNSolver(BaseDQNGameModel):

    def __init__(self):
        BaseDQNGameModel.__init__(self, "Deep Q Net", "deep_q_net", "dqn")

    def move(self, environment):
        BaseDQNGameModel.move(self, environment)
        pass


class DQNTrainer(BaseDQNGameModel):

    def __init__(self):
        BaseDQNGameModel.__init__(self, "Deep Q Net", "deep_q_net_trainer", "dqnt")

    def move(self, environment):
        pass
