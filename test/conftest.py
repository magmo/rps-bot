import pytest
from bot import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app_instance = create_app({
        'TESTING': True
    })

    yield app_instance

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
