from abc import ABC, abstractmethod


class RLAlgorithm(ABC):
    def __init__(self, seed: int = None):
        """
        Initialize the RL algorithm with any parameters or configurations.
        """
        pass

    @abstractmethod
    def get_action(self, user_id, state, parameters, decision_idx) -> tuple:
        """
        Generate an action based on the given user_id, state, decision index
        and model parameters. Return the action, probability of the action.
        """
        pass

    @abstractmethod
    def update(self, old_params, data) -> tuple:
        """
        Update the RL algorithm with new data and/or parameters.
        """
        pass

    @abstractmethod
    def make_state(self, context) -> tuple:
        """
        Create a state representation based on the context.
        """
        pass

    @abstractmethod
    def make_reward(self, user_id, state, action, outcome) -> tuple:
        """
        Create a reward based on the user_id, state, action and outcome.
        """
        pass