"""
Configuration settings for API automation tests
"""

# Base URL for JSONPlaceholder API
BASE_URL = "https://jsonplaceholder.typicode.com"

# API Endpoints
ENDPOINTS = {
    "posts": "/posts",
    "users": "/users",
    "comments": "/comments",
    "albums": "/albums",
    "photos": "/photos",
    "todos": "/todos"
}

# Test Data
TEST_POST = {
    "title": "Test Post Title",
    "body": "This is a test post body content for automation testing",
    "userId": 1
}

TEST_POST_UPDATE = {
    "title": "Updated Post Title",
    "body": "This is updated content",
    "userId": 1
}

# Timeout settings (in seconds)
REQUEST_TIMEOUT = 10
MAX_RESPONSE_TIME = 2.0

# Expected counts
TOTAL_POSTS = 100
TOTAL_USERS = 10
POSTS_PER_USER = 10

