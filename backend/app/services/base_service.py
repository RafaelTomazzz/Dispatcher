import os
import httpx
from urllib.parse import quote

from dotenv import load_dotenv
load_dotenv()

class GLPIBaseService:
    def __init__(self):
        self.base_url = os.getenv("DEFAULT_GLPI_URL")
        self.app_token = os.getenv("DEFAULT_APP_TOKEN")
        
        proxy_host = os.getenv("DEFAULT_PROXY_HOST")
        proxy_user = os.getenv("DEFAULT_PROXY_USER")
        proxy_pass = os.getenv("DEFAULT_PROXY_PASS")
        
        self.proxies: dict | None = None

        proxy_host = os.getenv("DEFAULT_PROXY_HOST")
        proxy_user = os.getenv("DEFAULT_PROXY_USER")
        proxy_pass = os.getenv("DEFAULT_PROXY_PASS")

        def is_set(v: str | None) -> bool:
            return bool(v) and v.strip() and v.strip().lower() != "none"

        if is_set(proxy_host):
            if is_set(proxy_user) and is_set(proxy_pass):
                proxy_url = f"http://{quote(proxy_user)}:{quote(proxy_pass)}@{proxy_host}"
                self.proxies = proxy_url
            else:
                proxy_url = f"http://{proxy_host}"
                self.proxies = proxy_url            
        
    def _get_headers(self, session_token: str = None):
        headers = {
            'Content-Type': 'application/json',
            'App-Token': self.app_token,
            'X-GLPI-Sanitized-Content': 'false'
        }
        if session_token:
            headers['Session-Token'] = session_token
        return headers
    
    async def get_async_client(self):
        return httpx.AsyncClient(proxy=self.proxies)