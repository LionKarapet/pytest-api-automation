"""
Posts Service - Handles all Posts API interactions
"""
from typing import Dict, Any, Optional, List
import requests
from config.settings import ENDPOINTS


class PostsService:
    """Service class for Posts API operations"""
    
    def __init__(self, api_client):
        """
        Initialize Posts Service
        
        Args:
            api_client: APIClient instance for making HTTP requests
        """
        self.api_client = api_client
        self.endpoint = ENDPOINTS['posts']
    
    def get_post_by_id(self, post_id: int) -> requests.Response:
        """
        Get a single post by ID
        
        Args:
            post_id: ID of the post to retrieve
            
        Returns:
            Response object
        """
        endpoint = f"{self.endpoint}/{post_id}"
        return self.api_client.get(endpoint)
    
    def get_all_posts(self) -> requests.Response:
        """
        Get all posts
        
        Returns:
            Response object with list of all posts
        """
        return self.api_client.get(self.endpoint)
    
    def get_posts_by_user(self, user_id: int) -> requests.Response:
        """
        Get posts filtered by user ID
        
        Args:
            user_id: ID of the user whose posts to retrieve
            
        Returns:
            Response object with filtered posts
        """
        params = {'userId': user_id}
        return self.api_client.get(self.endpoint, params=params)
    
    def create_post(self, post_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new post
        
        Args:
            post_data: Dictionary containing post data (title, body, userId)
            
        Returns:
            Response object with created post
        """
        return self.api_client.post(self.endpoint, post_data)
    
    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> requests.Response:
        """
        Update an existing post
        
        Args:
            post_id: ID of the post to update
            post_data: Dictionary containing updated post data
            
        Returns:
            Response object with updated post
        """
        endpoint = f"{self.endpoint}/{post_id}"
        return self.api_client.put(endpoint, post_data)
    
    def delete_post(self, post_id: int) -> requests.Response:
        """
        Delete a post
        
        Args:
            post_id: ID of the post to delete
            
        Returns:
            Response object
        """
        endpoint = f"{self.endpoint}/{post_id}"
        return self.api_client.delete(endpoint)

