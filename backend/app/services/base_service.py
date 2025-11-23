import os
import httpx

from dotenv import load_dotenv
load_dotenv()

class GLPIBaseService:
    def __init__(self):
        self.base_url = os.getenv("DEFAULT_GLPI_URL")
        self.app_token = os.getenv("DEFAULT_APP_TOKEN")
        
        proxy_host = os.getenv("DEFAULT_PROXY_HOST")
        proxy_user = os.getenv("DEFAULT_PROXY_USER")
        proxy_pass = os.getenv("DEFAULT_PROXY_PASS")
        
        self.proxies = None

        if proxy_host and proxy_host != "None":
            if proxy_user and proxy_pass:
                proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}"
            else:
                proxy_url = f"http://{proxy_host}"
            
            # 3. Store it for httpx
            self.proxies = {
                "http://": proxy_url,
                "https://": proxy_url
            }
        
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