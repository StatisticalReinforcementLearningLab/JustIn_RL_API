import random
from app.algorithms.base import RLAlgorithm


class FlatProbRLAlgorithm(RLAlgorithm):
    def __init__(self, *args, **kwargs):
        """
        Initialize the stateless RL algorithm.
        """
        super().__init__(*args, **kwargs)
        self.config = kwargs.get("config", {})

    def get_action(self, user_id, context):
        """
        Generate an action based on the context and user_id.
        """
        # Stateless, so we ignore the context and user_id
        return random.choice([0, 1])

    def update(self, *args, **kwargs):
        """
        Since this is a stateless algorithm, update does nothing.
        """
        pass
