"""
Test cases for Users API endpoints
"""
import pytest
from utils.helpers import validate_user_schema
from config.settings import TOTAL_USERS


class TestUsersAPI:
    """Test suite for Users API endpoints"""
    
    @pytest.mark.positive
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_get_user_details(self, users_service, user_id):
        """
        TC-008: Verify retrieval of user information (parametrized test)
        
        Validations:
        - Status code is 200
        - Schema validation for user object
        - Nested object validation (address, geo, company)
        - Data type validation
        """
        # Act
        response = users_service.get_user_by_id(user_id)
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        user_data = response.json()
        
        # Validate user schema
        assert validate_user_schema(user_data), f"User {user_id} schema validation failed"
        
        # Validate user ID
        assert user_data['id'] == user_id, f"Expected user id {user_id}, got {user_data['id']}"
        
        # Validate data types
        assert isinstance(user_data['name'], str), "Name should be string"
        assert isinstance(user_data['username'], str), "Username should be string"
        assert isinstance(user_data['email'], str), "Email should be string"
        
        # Validate email format
        assert '@' in user_data['email'], "Email should contain @"
        
        # Validate nested address object
        assert 'address' in user_data, "User should have address"
        assert 'geo' in user_data['address'], "Address should have geo coordinates"
        assert 'lat' in user_data['address']['geo'], "Geo should have latitude"
        assert 'lng' in user_data['address']['geo'], "Geo should have longitude"
        
        # Validate nested company object
        assert 'company' in user_data, "User should have company"
        assert 'name' in user_data['company'], "Company should have name"
    
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_all_users(self, users_service):
        """
        Verify retrieval of all users
        
        Validations:
        - Status code is 200
        - Response is a list
        - Response count matches expected total
        - All users have valid schema
        """
        # Act
        response = users_service.get_all_users()
        
        # Assert
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        users = response.json()
        
        # Validate response type
        assert isinstance(users, list), "Response should be a list"
        
        # Validate count
        assert len(users) == TOTAL_USERS, f"Expected {TOTAL_USERS} users, got {len(users)}"
        
        # Validate all users have valid schema
        for user in users:
            assert validate_user_schema(user), f"User {user['id']} has invalid schema"
    
    @pytest.mark.negative
    def test_get_user_not_found(self, users_service):
        """
        Verify handling of non-existent user
        
        Validations:
        - Status code is 404
        - Error response handling
        """
        # Arrange
        invalid_user_id = 9999
        
        # Act
        response = users_service.get_user_by_id(invalid_user_id)
        
        # Assert
        assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"

