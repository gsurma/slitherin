
import copy
from game.helpers.run import Run
from game.models.domain_specific.dnn_ai_solver import BaseDNNGameModel


class DNNMonteCarloSolver(BaseDNNGameModel):

    model = None

    def __init__(self):
        BaseDNNGameModel.__init__(self, "Deep Neural Net MC", "deep_neural_net_monte_carlo", "dnnmc")

    def move(self, environment):
        BaseDNNGameModel.move(self, environment)
        possible_actions = environment.possible_actions_for_current_action(environment.snake_action)
        runs = []
        for action in possible_actions:
            new_environment = copy.deepcopy(environment)
            score = self._run(action, new_environment)
            runs.append(Run(action, score))
        return self._best_action_for_runs(runs)

    def _run(self, action, environment):
        score = self._deep_neural_net_driven_gameplay(environment, action)
        return score

    def _deep_neural_net_driven_gameplay(self, environment, action):
        new_action = action
        while environment.step(new_action):
            environment.eat_fruit_if_possible()
            new_action = self._predict(environment, self.model)
        return environment.reward()
