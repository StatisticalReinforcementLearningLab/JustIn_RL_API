import subprocess
import logging
import pickle
from flask import Flask, request, jsonify
from app.extensions import db, migrate
from app.logging_config import setup_logging
from app.algorithms.flat_prob import FlatProbRLAlgorithm
from app.models import ModelParameters


def create_app(config_class="config.Config"):
    """
    Factory function to create and configure the Flask app.
    """
    # Set up logging
    setup_logging()
    logger = logging.getLogger()
    logger.info("Starting Flask application...")

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database and migration extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Create a shared instance of the Flat Probability RL Algorithm
    app.rl_algorithm = FlatProbRLAlgorithm()

    # Register blueprints
    from app.routes.user import user_blueprint
    from app.routes.action import action_blueprint
    from app.routes.data import data_blueprint
    from app.routes.update import update_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/api/v1")
    app.register_blueprint(action_blueprint, url_prefix="/api/v1")
    app.register_blueprint(data_blueprint, url_prefix="/api/v1")
    app.register_blueprint(update_blueprint, url_prefix="/api/v1")

    # Log incoming requests and outgoing responses
    @app.before_request
    def log_request_info():
        logging.info(
            "Request: method=%s path=%s args=%s body=%s",
            request.method,
            request.path,
            request.args,
            request.get_data(as_text=True),
        )

    @app.after_request
    def log_response_info(response):
        logging.info(
            "Response: status=%s body=%s",
            response.status,
            response.get_data(as_text=True),
        )
        return response
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Catch all unhandled exceptions, log them, and return a 500 error.
        """
        logger.error("Unhandled Exception: %s", str(e), exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
    
    @app.before_first_request
    def initialize_model_parameters():
        """
        Initialize the ModelParameters table with default priors if empty.
        """
        if not ModelParameters.query.first():
            # Load priors from config or pickle file
            pickle_file = app.config["PRIORS_PICKLE_FILE"]
            priors = app.config["MODEL_PRIORS"]

            if pickle_file:
                try:
                    with open(pickle_file, "rb") as f:
                        priors = pickle.load(f)
                    app.logger.info("Loaded priors from pickle file: %s", pickle_file)
                except Exception as e:
                    app.logger.error("Failed to load priors from pickle file: %s", str(e))
                    raise e

            # Initialize the ModelParameters table
            default_params = ModelParameters(probability_of_action=priors["probability_of_action"])
            db.session.add(default_params)
            db.session.commit()
            app.logger.info("Initialized ModelParameters with priors: %s", priors)

    with app.app_context():
        # Create tables for models
        db.create_all()

    # Register CLI commands
    register_cli_commands(app)

    return app


def register_cli_commands(app):
    """
    Registers custom CLI commands with the Flask app.
    """

    @app.cli.command("reset-db")
    def reset_db():
        """
        Drops all tables and recreates them using migrations.
        """
        print("Dropping all tables...")
        db.drop_all()
        db.session.commit()

        print("Recreating all tables...")
        subprocess.run(["flask", "db", "upgrade"], check=True)
        print("Database reset complete.")
