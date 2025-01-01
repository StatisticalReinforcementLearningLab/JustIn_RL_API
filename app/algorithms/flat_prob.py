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

    def get_action(
        self, user_id: str, state: dict, parameters: dict, decision_idx: int
    ) -> tuple[int, float, dict]:
        """
        Generate an action based on the state and user_id.
        """
        # Flat probability, so we ignore the state, user_id, and decision_idx
        self.logger.info(
            "Getting action for user_id=%s with state=%s at decision_idx=%d",
            user_id,
            state,
            decision_idx,
        )

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

    def update(self, old_params: dict, data: dict) -> tuple[bool, dict]:
        """
        This method is used to update the algorithm with collected data.
        For this example, we will either increase or decrease the probability
        based on the average temperature. If it is less than 30, we increase
        the probability by 0.01, otherwise we decrease it by 0.01.
        """
        try:
            # For the flat probability algorithm, there is no update
            # Get the old parameters
            probability_of_action = old_params["probability_of_action"]

            # Get the temperature from the data
            temperature = data["temperatures"]

            # For this example, we will either increase or decrease the probability
            # based on the average temperature. If it is less than 30, we increase
            # the probability by 0.01, otherwise we decrease it by 0.01.
            if np.mean(temperature) < 30:
                probability_of_action += 0.01
            else:
                probability_of_action -= 0.01

            # Clipping the probability to be within the range [0.2, 0.8]
            probability_of_action = max(0.2, min(0.8, probability_of_action))

            # Return the new parameters
            new_params = {"probability_of_action": probability_of_action}
            return True, new_params

        except Exception as e:
            # Log the error
            self.logger.error(f"Error in updating model: {e}")
            return False, old_params

    def make_state(self, context: dict) -> tuple[bool, list]:
        """
        Create a state representation based on the context.
        """

        # For the flat probability algorithm, there is no state
        # But we return the temperature as a placeholder
        # for the template

        try:
            state = [context["temperature"]]
            return True, state
        except Exception as e:
            self.logger.error(f"Error in making state: {e}")
            return False, []

    def make_reward(
        self, user_id: str, state: dict, action: int, outcome: dict
    ) -> tuple[int, float]:
        """
        Create a reward based on the user_id, state, and action.
        """
        # For the flat probability algorithm, there is no reward
        # But we return the number of clicks as a placeholder
        # for this template

        try:
            reward = outcome["clicks"]
            return True, reward
        except Exception as e:
            self.logger.error(f"Error in making reward: {e}")
            return False, None

