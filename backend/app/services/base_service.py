import os
import httpx
from dotenv import load_dotenv

load_dotenv()

class GLPIBaseService:
    def __init__(self):
        self.base_url = os.getenv("DEFAULT_GLPI_URL")
        self.app_token = os.getenv("DEFAULT_APP_TOKEN")
        self.proxy_url = os.getenv("DEFAULT_PROXY")

    def _get_headers(self, session_token: str = None):
        headers = {
            'Content-Type': 'application/json',
            'App-Token': self.app_token
        }
        if session_token:
            headers['Session-Token'] = session_token
        return headers
    
    def _get_proxies(self, user: str = None, password: str = None):
        proxy_mounts = {}
        # Normalize proxy_url if the string "None" was used
        proxy_url = None if self.proxy_url in (None, "None", "") else self.proxy_url

        if proxy_url:
            if user and password:
                proxy_mounts = {
                    "http://": f"{user}:{password}@{proxy_url}",
                    "https://": f"{user}:{password}@{proxy_url}"
                }
            else:
                proxy_mounts = {
                    "http://": proxy_url,
                    "https://": proxy_url
                }
        return proxy_mounts

    async def get_async_client(self, user: str = None, password: str = None):
        # Returns an httpx client configured with your proxy
        return httpx.AsyncClient(proxies=self._get_proxies(user, password))