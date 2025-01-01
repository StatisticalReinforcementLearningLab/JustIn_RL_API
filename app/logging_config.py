import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configures the logging for the Flask application.
    """
    # Ensure the logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Set up rotating file handler
    log_file = os.path.join(log_dir, "app.log")
    handler = RotatingFileHandler(log_file, maxBytes=100 * 1024 * 1024, backupCount=5000)  # 100 MB per file
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            handler,              # Log to file in logs directory
            logging.StreamHandler()  # Log to console
        ]
    )

def get_rl_logger():
    """
    Returns a logger for the RL Algorithm with a dedicated file handler.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    rl_log_file = os.path.join(log_dir, "rl.log")
    rl_handler = RotatingFileHandler(rl_log_file, maxBytes=100 * 1024 * 1024, backupCount=5000)  # 100 MB per file
    rl_handler.setLevel(logging.INFO)
    rl_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [RL] %(message)s")
    rl_handler.setFormatter(rl_formatter)

    rl_logger = logging.getLogger("RLAlgorithm")
    rl_logger.setLevel(logging.INFO)
    rl_logger.addHandler(rl_handler)

    return rl_logger