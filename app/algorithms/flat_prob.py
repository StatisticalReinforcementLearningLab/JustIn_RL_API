import random
import numpy as np
from app.algorithms.base import RLAlgorithm
from app.logging_config import get_rl_logger


class FlatProbRLAlgorithm(RLAlgorithm):
    """
    A flat probability algorithm that generates actions with a fixed probability.
    """

    def __init__(self, seed: int = None):
        """
        Initialize the flat probability RL algorithm.
        """
        super().__init__(seed)
        self.logger = get_rl_logger()
        self.seed = seed
        self.rng = np.random.default_rng(
            self.seed
        )  # Use NumPy's RNG for reproducibility
        self.logger.info("Flat Probability RL Algorithm initialized.")

    def get_action(self, user_id: str, state: dict, parameters: dict) -> tuple:
        """
        Generate an action based on the state and user_id.
        """
        # Flat probability, so we ignore the state and user_id
        self.logger.info("Getting action for user_id=%s with state=%s", user_id, state)

        # Capture the rng state for reproducibility
        rng_state = self.rng.bit_generator.state

        # Get the model parameters
        # In this case, it is nothing but the flat probability
        probability = parameters["probability"]

        # Use bernoulli distribution to generate an action
        action = self.rng.binomial(1, probability)

        # Log the generated action
        self.logger.info(
            "Generated action=%d for user_id=%s with probability=%f",
            action,
            user_id,
            probability,
        )

        return action, probability, rng_state

    def update(self, *args, **kwargs):
        """
        This method is used to update the algorithm with collected data.
        Since this is a fixed algorithm, so update does nothing.
        """
        pass

    def make_state(self, context: dict) -> list:
        """
        Create a state representation based on the context.
        """

        # For the flat probability algorithm, there is no state
        # But we return the temperature as a placeholder
        # for the template

        state = [context["temperature"]]
        return state

    def make_reward(
        self, user_id: str, state: dict, action: int, outcome: dict
    ) -> float:
        """
        Create a reward based on the user_id, state, and action.
        """
        # For the flat probability algorithm, there is no reward
        # But we return 0.0 as a placeholder for the template

        return 0.0
