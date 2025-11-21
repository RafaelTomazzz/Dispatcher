import httpx
import os
import base64
from fastapi import HTTPException

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DEFAULT_GLPI_URL = os.getenv("DEFAULT_GLPI_URL")
DEFAULT_APP_TOKEN = os.getenv("DEFAULT_APP_TOKEN")
DEFAULT_PROXY = os.getenv("DEFAULT_PROXY")

class GlpiService:
    async def init_session(
        self,
        login: str,
        password: str
    ) -> str:
        """
        Authenticate against GLPI API and return session_token or error message.
        
        Args:
            login: GLPI username.
            password: GLPI password.
            app_token: Optional App-Token for API client.
        
        Returns:
            String of session_token or dict with status code and error_message.
        """
              
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Basic {base64.b64encode(f"{login}:{password}".encode()).decode()}"
        }
        
        if DEFAULT_APP_TOKEN != "None":
            headers['App-Token'] = DEFAULT_APP_TOKEN
        
        if DEFAULT_PROXY != "None":
            proxy = f"http://{login}:{password}@{DEFAULT_PROXY}"
        else:
            proxy = None
        
        async with httpx.AsyncClient(proxy=proxy) as client:
            try:
                response = await client.get(f"{DEFAULT_GLPI_URL}/initSession", headers=headers)
                
                # Handle GLPI Errors (400, 401, etc.)
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, 
                        detail=f"GLPI Login Failed: {response.text}"
                    )

                data = response.json()
                return data.get("session_token")

            except httpx.RequestError as exc:
                raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")

# Create a singleton instance to be imported elsewhere
glpi_service = GlpiService()