import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app_instance = create_app()
    app_instance.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # Use an in-memory database for tests
    )

    with app_instance.app_context():
        # Initialize database or other setup here if needed
        yield app_instance
        db.session.remove()
        db.drop_all()  # Drop all tables after the test is completed

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
