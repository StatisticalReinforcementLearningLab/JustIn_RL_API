import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app_instance = create_app()

    # Use the testing configuration
    app_instance.config.from_object("config.TestingConfig")

    with app_instance.app_context():
        # Initialize database or other setup here if needed
        yield app_instance
        db.session.remove()
        db.drop_all()  # Drop all tables after the test is completed

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
