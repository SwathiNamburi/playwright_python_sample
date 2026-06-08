import requests
import json
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(url, data=data, json=json_data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.put(url, data=data, json=json_data)

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.delete(url)

    def set_auth(self, token: str, auth_type: str = 'Bearer'):
        self.session.headers['Authorization'] = f"{auth_type} {token}"

    def get_json(self, response: requests.Response) -> Dict[str, Any]:
        return response.json()

    def get_text(self, response: requests.Response) -> str:
        return response.text
