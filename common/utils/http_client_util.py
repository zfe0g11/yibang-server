import requests
from typing import Dict, Optional, Any


class HttpClientUtil:
    @staticmethod
    def get(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.get(url, params=params, headers=headers)
    
    @staticmethod
    def post(url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.post(url, data=data, json=json, headers=headers)
    
    @staticmethod
    def put(url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.put(url, data=data, json=json, headers=headers)
    
    @staticmethod
    def delete(url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return requests.delete(url, headers=headers)