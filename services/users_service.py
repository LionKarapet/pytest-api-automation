"""
Users Service - Handles all Users API interactions
"""
from typing import Dict, Any, Optional, List
import requests
from config.settings import ENDPOINTS


class UsersService:
    """Service class for Users API operations"""
    
    def __init__(self, api_client):
        """
        Initialize Users Service
        
        Args:
            api_client: APIClient instance for making HTTP requests
        """
        self.api_client = api_client
        self.endpoint = ENDPOINTS['users']
    
    def get_user_by_id(self, user_id: int) -> requests.Response:
        """
        Get a single user by ID
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            Response object
        """
        endpoint = f"{self.endpoint}/{user_id}"
        return self.api_client.get(endpoint)
    
    def get_all_users(self) -> requests.Response:
        """
        Get all users
        
        Returns:
            Response object with list of all users
        """
        return self.api_client.get(self.endpoint)
    
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new user
        
        Args:
            user_data: Dictionary containing user data
            
        Returns:
            Response object with created user
        """
        return self.api_client.post(self.endpoint, user_data)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> requests.Response:
        """
        Update an existing user
        
        Args:
            user_id: ID of the user to update
            user_data: Dictionary containing updated user data
            
        Returns:
            Response object with updated user
        """
        endpoint = f"{self.endpoint}/{user_id}"
        return self.api_client.put(endpoint, user_data)
    
    def delete_user(self, user_id: int) -> requests.Response:
        """
        Delete a user
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            Response object
        """
        endpoint = f"{self.endpoint}/{user_id}"
        return self.api_client.delete(endpoint)

