import subprocess
from app.extensions import db, migrate
from flask import Flask


def create_app(config_class="config.Config"):
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database and migration extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.users import users_blueprint
    from app.routes.actions import actions_blueprint
    from app.routes.data import data_blueprint
    from app.routes.updates import updates_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/api/v1")
    app.register_blueprint(actions_blueprint, url_prefix="/api/v1")
    app.register_blueprint(data_blueprint, url_prefix="/api/v1")
    app.register_blueprint(updates_blueprint, url_prefix="/api/v1")

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