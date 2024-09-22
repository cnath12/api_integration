import requests
from typing import Dict, Any, Optional, Union
from utils.rate_limiter import RateLimiter
from utils.retry_mechanism import retry_with_exponential_backoff
from db.database import DatabaseManager
from config import COSMOS_CONFIG

class BaseApiClient:
    def __init__(self, base_url: str, auth_method: str, auth_params: Dict[str, Any], cosmos_config: Dict[str, Any]):
        self.base_url = base_url
        self.session = requests.Session()
        self.rate_limiter = RateLimiter()
        self.db_manager = DatabaseManager(**cosmos_config)
        
        if auth_method == "basic":
            from auth.basic_auth import BasicAuth
            self.auth = BasicAuth(**auth_params)
        elif auth_method == "api_key":
            from auth.api_key_auth import ApiKeyAuth
            self.auth = ApiKeyAuth(**auth_params)
        elif auth_method == "oauth2":
            from auth.oauth2_auth import OAuth2Auth
            self.auth = OAuth2Auth(**auth_params)
        elif auth_method == "none":
            self.auth = None
        else:
            raise ValueError("Unsupported authentication method")

    @retry_with_exponential_backoff()
    def request(self, method: str, endpoint: str, **kwargs) -> Union[Dict[str, Any], requests.Response]:
        url = f"{self.base_url}/{endpoint}"
        headers = kwargs.pop("headers", {})
        if self.auth:
            headers.update(self.auth.get_auth_header())

        with self.rate_limiter:
            response = self.session.request(method, url, headers=headers, **kwargs)
        
        response.raise_for_status()
        
        if response.headers.get('content-type') == 'application/json':
            return response.json()
        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.request("GET", endpoint, params=params)
        if endpoint.startswith("users"):
            user_id = endpoint.split('/')[-1]
            self.db_manager.create_item({"id": user_id, **response})
        return response

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # response = self.request("POST", endpoint, json=data)
        response = {
            "id": data["id"],
            "name": data['name'],
            "email": data['email'],
            "job": data["job"]
            }
        if endpoint == "users":
            self.db_manager.create_item(response)
        return response

    def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.request("PUT", endpoint, json=data)
        if endpoint.startswith("users"):
            user_id = endpoint.split('/')[-1]
            self.db_manager.update_item(user_id, response)
        return response

    def delete(self, endpoint: str) -> requests.Response:
        response = self.request("DELETE", endpoint)
        if endpoint.startswith("users"):
            user_id = endpoint.split('/')[-1]
            self.db_manager.delete_item(user_id, user_id)
        return response

    def __del__(self):
        pass