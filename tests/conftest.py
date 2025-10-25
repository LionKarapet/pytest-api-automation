"""
Pytest configuration and fixtures
"""
import pytest
from utils.helpers import APIClient
from services import PostsService, UsersService


@pytest.fixture(scope="session")
def api_client():
    """
    Fixture to provide API client instance for all tests
    
    Returns:
        APIClient instance
    """
    return APIClient()


@pytest.fixture(scope="session")
def posts_service(api_client):
    """
    Fixture to provide Posts Service instance for all tests
    
    Args:
        api_client: APIClient fixture
        
    Returns:
        PostsService instance
    """
    return PostsService(api_client)


@pytest.fixture(scope="session")
def users_service(api_client):
    """
    Fixture to provide Users Service instance for all tests
    
    Args:
        api_client: APIClient fixture
        
    Returns:
        UsersService instance
    """
    return UsersService(api_client)


@pytest.fixture(scope="function")
def sample_post_data():
    """
    Fixture to provide sample post data for testing
    
    Returns:
        Dictionary with post data
    """
    return {
        "title": "Test Automation Post",
        "body": "This is a test post created by automated testing framework",
        "userId": 1
    }


@pytest.fixture(scope="function")
def sample_update_data():
    """
    Fixture to provide sample update data for testing
    
    Returns:
        Dictionary with updated post data
    """
    return {
        "id": 1,
        "title": "Updated Title via Automation",
        "body": "This post has been updated by automated tests",
        "userId": 1
    }

