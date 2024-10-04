import requests
from app.utils.logging import logger
import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_call(self, endpoint, method, headers=None, data="", json={}, params={}):
        url = self.base_url + endpoint
        logger.info(f"Making request to {url}")
        
        payload = json or data
        
        response = requests.request(method, url, headers=headers, json=payload, params=params)
        
        logger.info(f"Response received: {response.json()}")
        return response