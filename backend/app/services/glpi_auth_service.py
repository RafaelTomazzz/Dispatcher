import base64
from fastapi import HTTPException
from .base_service import GLPIBaseService

class AuthService(GLPIBaseService):
    
    async def init_session(
        self,
        login: str,
        password: str
    ) -> str:
        """
        Authenticate against GLPI API and return session_token.
        
        Args:
            login: GLPI username.
            password: GLPI password.
        
        Returns:
            String of session_token or HTTP exception.
        """
        
        client = await self.get_async_client(user, password)
        url = f"{self.base_url}/initSession"
        
        headers = self._get_headers()
        headers['Authorization']: f"Basic {base64.b64encode(f"{login}:{password}".encode()).decode()}"
        
        try:
            response = await client.get(url, headers=headers)
            
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
        finally:
            await client.aclose()

# Create a singleton instance to be imported elsewhere
auth_service = AuthService()