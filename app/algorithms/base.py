from abc import ABC, abstractmethod


class RLAlgorithm(ABC):
    def __init__(self, *args, **kwargs):
        """
        Initialize the RL algorithm with any parameters or configurations.
        """
        pass

    @abstractmethod
    def get_action(self, user_id, context):
        """
        Generate an action based on the given user_id and context.
        """
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Update the RL algorithm with new data or parameters.
        """
        pass
