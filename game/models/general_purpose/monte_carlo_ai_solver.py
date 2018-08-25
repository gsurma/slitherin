import random
import copy
from game.helpers.run import Run
from game.models.base_game_model import BaseGameModel


class MonteCarloSolver(BaseGameModel):

    def __init__(self, runs=1000):
        BaseGameModel.__init__(self, "Monte Carlo", "monte_carlo", "mc")
        self.runs = runs

    def move(self, environment):
        possible_actions = environment.possible_actions_for_current_action(environment.snake_action)
        runs = []
        for run_index in range(0, self.runs):
            action = random.choice(possible_actions)
            new_environment = copy.deepcopy(environment)
            score = self._run(action, new_environment)
            runs.append(Run(action,score))
        return self._best_action_for_runs(runs)

    def _run(self, action, environment):
        score = self._random_gameplay(environment, action)
        return score

    def _random_gameplay(self, environment, action):
        new_action = action
        while environment.step(new_action):
            environment.eat_fruit_if_possible()
            new_action = random.choice(environment.possible_actions_for_current_action(environment.snake_action))
        return environment.reward()
