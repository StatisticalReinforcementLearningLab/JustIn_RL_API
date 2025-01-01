from abc import ABC, abstractmethod


class RLAlgorithm(ABC):
    def __init__(self, seed: int = None):
        """
        Initialize the RL algorithm with any parameters or configurations.
        """
        pass

    @abstractmethod
    def get_action(self, user_id, state, parameters) -> tuple:
        """
        Generate an action based on the given user_id and state.
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs) -> tuple:
        """
        Update the RL algorithm with new data or parameters.
        """
        pass

    @abstractmethod
    def make_state(self, context) -> dict:
        """
        Create a state representation based on the context.
        """
        pass

    @abstractmethod
    def make_reward(self, user_id, state, action, observation) -> float:
        """
        Create a reward based on the user_id, state, action and observation.
        """
        pass