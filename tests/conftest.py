import pytest
from app import create_app, db


@pytest.fixture(scope="module")
def test_client():
    """
    Creates a Flask test client with a temporary SQLite database.
    """
    # Configure the app for testing
    app = create_app()
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # In-memory database
        TESTING=True,
    )

    # Establish an application context before running tests
    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()  # Return the Flask test client
        db.session.remove()
        db.drop_all()  # Drop all tables after tests
