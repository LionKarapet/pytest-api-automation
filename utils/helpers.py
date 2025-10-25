"""
Helper functions for API testing
"""
import requests
from typing import Dict, Any, Optional
from config.settings import BASE_URL, REQUEST_TIMEOUT


class APIClient:
    """API Client for making HTTP requests"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.timeout = REQUEST_TIMEOUT
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, timeout=self.timeout)
        return response
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Request body data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, timeout=self.timeout)
        return response
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """
        Make PUT request
        
        Args:
            endpoint: API endpoint
            data: Request body data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data, timeout=self.timeout)
        return response
    
    def delete(self, endpoint: str) -> requests.Response:
        """
        Make DELETE request
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, timeout=self.timeout)
        return response


def validate_response_schema(response_data: Dict, expected_fields: list) -> bool:
    """
    Validate response contains expected fields
    
    Args:
        response_data: Response JSON data
        expected_fields: List of expected field names
        
    Returns:
        True if all fields present, False otherwise
    """
    return all(field in response_data for field in expected_fields)


def validate_post_schema(post_data: Dict) -> bool:
    """
    Validate post object schema
    
    Args:
        post_data: Post object data
        
    Returns:
        True if valid schema, False otherwise
    """
    required_fields = ['userId', 'id', 'title', 'body']
    
    # Check all required fields present
    if not validate_response_schema(post_data, required_fields):
        return False
    
    # Validate data types
    if not isinstance(post_data['userId'], int):
        return False
    if not isinstance(post_data['id'], int):
        return False
    if not isinstance(post_data['title'], str):
        return False
    if not isinstance(post_data['body'], str):
        return False
    
    return True


def validate_user_schema(user_data: Dict) -> bool:
    """
    Validate user object schema
    
    Args:
        user_data: User object data
        
    Returns:
        True if valid schema, False otherwise
    """
    required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
    
    # Check all required fields present
    if not validate_response_schema(user_data, required_fields):
        return False
    
    # Validate nested address object
    if 'address' in user_data:
        address_fields = ['street', 'suite', 'city', 'zipcode', 'geo']
        if not validate_response_schema(user_data['address'], address_fields):
            return False
        
        # Validate nested geo object
        if 'geo' in user_data['address']:
            geo_fields = ['lat', 'lng']
            if not validate_response_schema(user_data['address']['geo'], geo_fields):
                return False
    
    # Validate nested company object
    if 'company' in user_data:
        company_fields = ['name', 'catchPhrase', 'bs']
        if not validate_response_schema(user_data['company'], company_fields):
            return False
    
    return True


def validate_response_time(response: requests.Response, max_time: float) -> bool:
    """
    Validate response time is within acceptable range
    
    Args:
        response: Response object
        max_time: Maximum acceptable time in seconds
        
    Returns:
        True if within limit, False otherwise
    """
    response_time = response.elapsed.total_seconds()
    return response_time < max_time

