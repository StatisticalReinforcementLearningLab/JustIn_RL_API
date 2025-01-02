import os


class Config:
    # General Configuration
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,  # Recycle connections after 3600 seconds (1 hour)
    }
    RL_ALGORITHM_SEED = 42  # Seed for RL Algorithm random state

    # Prior Configuration
    # If you specify a pickle file, it should be a dictionary with the same keys
    # as the entries in the ModelParameters table. Otherwise, see the next setting
    # to specify the individual keys in text format.
    PRIORS_PICKLE_FILE = None  # Path to the pickled priors file

    # If you don't want to use a pickle file, you can specify the priors directly
    # using the following format. The keys should match the entries in the
    # ModelParameters table.
    MODEL_PRIORS = {
        "probability_of_action": 0.5,
    }

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
