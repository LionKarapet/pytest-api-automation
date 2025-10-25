"""
Test cases for Posts API endpoints
"""
import pytest
from utils.helpers import (
    validate_post_schema,
    validate_response_time
)
from config.settings import (
    TOTAL_POSTS,
    POSTS_PER_USER,
    MAX_RESPONSE_TIME
)


class TestPostsAPI:
    """Test suite for Posts API endpoints"""
    
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_single_post(self, posts_service):
        """
        TC-001: Verify retrieval of a single post by ID
        
        Validations:
        - Status code is 200
        - Response schema is valid
        - Data types are correct
        - Specific fields contain expected values
        """
        # Arrange
        post_id = 1
        
        # Act
        response = posts_service.get_post_by_id(post_id)
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        post_data = response.json()
        
        # Validate schema
        assert validate_post_schema(post_data), "Response schema validation failed"
        
        # Validate specific data
        assert post_data['id'] == post_id, f"Expected post id {post_id}, got {post_data['id']}"
        assert post_data['userId'] > 0, "userId should be greater than 0"
        assert len(post_data['title']) > 0, "Title should not be empty"
        assert len(post_data['body']) > 0, "Body should not be empty"
    
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_all_posts(self, posts_service):
        """
        TC-002: Verify retrieval of all posts
        
        Validations:
        - Status code is 200
        - Response is a list
        - Response count matches expected total
        - All items have valid schema
        """
        # Act
        response = posts_service.get_all_posts()
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        posts = response.json()
        
        # Validate response type
        assert isinstance(posts, list), "Response should be a list"
        
        # Validate count
        assert len(posts) == TOTAL_POSTS, f"Expected {TOTAL_POSTS} posts, got {len(posts)}"
        
        # Validate first post schema
        assert validate_post_schema(posts[0]), "First post schema validation failed"
        
        # Validate last post schema
        assert validate_post_schema(posts[-1]), "Last post schema validation failed"
    
    @pytest.mark.positive
    def test_create_new_post(self, posts_service, sample_post_data):
        """
        TC-003: Verify creation of a new post
        
        Validations:
        - Status code is 201 (Created)
        - Response contains assigned ID
        - Posted data is present in response
        - Response schema is valid
        """
        # Act
        response = posts_service.create_post(sample_post_data)
        
        # Assert
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        
        created_post = response.json()
        
        # Validate ID assignment
        assert 'id' in created_post, "Response should contain assigned ID"
        assert created_post['id'] > 0, "Assigned ID should be greater than 0"
        
        # Validate posted data
        assert created_post['title'] == sample_post_data['title'], "Title mismatch"
        assert created_post['body'] == sample_post_data['body'], "Body mismatch"
        assert created_post['userId'] == sample_post_data['userId'], "UserId mismatch"
    
    @pytest.mark.positive
    def test_update_post(self, posts_service, sample_update_data):
        """
        TC-004: Verify updating an existing post
        
        Validations:
        - Status code is 200
        - Updated fields reflect changes
        - Response contains all required fields
        """
        # Arrange
        post_id = sample_update_data['id']
        
        # Act
        response = posts_service.update_post(post_id, sample_update_data)
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        updated_post = response.json()
        
        # Validate updated data
        assert updated_post['id'] == post_id, "Post ID should not change"
        assert updated_post['title'] == sample_update_data['title'], "Title was not updated"
        assert updated_post['body'] == sample_update_data['body'], "Body was not updated"
        assert updated_post['userId'] == sample_update_data['userId'], "UserId should match"
    
    @pytest.mark.positive
    def test_delete_post(self, posts_service):
        """
        TC-005: Verify deletion of a post
        
        Validations:
        - Status code is 200
        - Response body is empty/valid
        """
        # Arrange
        post_id = 1
        
        # Act
        response = posts_service.delete_post(post_id)
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        # JSONPlaceholder returns empty object on delete
        deleted_response = response.json()
        assert isinstance(deleted_response, dict), "Response should be a dictionary"
    
    @pytest.mark.negative
    def test_get_post_not_found(self, posts_service):
        """
        TC-006: Verify handling of non-existent post
        
        Validations:
        - Status code is 404
        - Error response is handled properly
        """
        # Arrange
        invalid_post_id = 9999
        
        # Act
        response = posts_service.get_post_by_id(invalid_post_id)
        
        # Assert
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"
        
        # Validate error response
        error_response = response.json()
        assert isinstance(error_response, dict), "Error response should be a dictionary"
    
    @pytest.mark.positive
    @pytest.mark.parametrize("user_id,expected_count", [
        (1, POSTS_PER_USER),
        (2, POSTS_PER_USER),
        (3, POSTS_PER_USER),
        (4, POSTS_PER_USER),
    ])
    def test_get_posts_by_user(self, posts_service, user_id, expected_count):
        """
        TC-007: Verify filtering posts by user ID (parametrized test)
        
        Validations:
        - Status code is 200
        - Filter parameter works correctly
        - All returned posts belong to requested user
        - Post count matches expected value
        """
        # Act
        response = posts_service.get_posts_by_user(user_id)
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        posts = response.json()
        
        # Validate response is list
        assert isinstance(posts, list), "Response should be a list"
        
        # Validate count
        assert len(posts) == expected_count, f"Expected {expected_count} posts for user {user_id}, got {len(posts)}"
        
        # Validate all posts belong to the requested user
        for post in posts:
            assert post['userId'] == user_id, f"Found post with userId {post['userId']}, expected {user_id}"
            assert validate_post_schema(post), f"Post {post['id']} has invalid schema"
    
    @pytest.mark.negative
    def test_invalid_post_creation(self, posts_service):
        """
        TC-009: Verify validation with invalid/incomplete data
        
        Note: JSONPlaceholder accepts all data, but we test the behavior
        
        Validations:
        - Status code handling
        - Response validation
        """
        # Arrange
        invalid_data = {
            "title": "",  # Empty title
            "body": "",   # Empty body
        }
        
        # Act
        response = posts_service.create_post(invalid_data)
        
        # Assert
        # JSONPlaceholder will still return 201, but in real API this might be 400
        assert response.status_code in [200, 201, 400], "Status code should be valid"
        
        # Validate response structure
        response_data = response.json()
        assert isinstance(response_data, dict), "Response should be a dictionary"
    
    @pytest.mark.performance
    def test_response_time(self, posts_service):
        """
        TC-010: Verify API response time performance
        
        Validations:
        - Response time is within acceptable threshold
        - Status code is 200
        """
        # Act
        response = posts_service.get_all_posts()
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        # Validate response time
        assert validate_response_time(response, MAX_RESPONSE_TIME), \
            f"Response time {response.elapsed.total_seconds()}s exceeded maximum {MAX_RESPONSE_TIME}s"
        
        print(f"\n✓ Response time: {response.elapsed.total_seconds():.3f}s")

