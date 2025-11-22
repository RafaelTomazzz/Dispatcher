import base64
import httpx
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
        
        client = await self.get_async_client()
        url = f"{self.base_url}/initSession"
        
        headers = self._get_headers()
        cred = f"{login}:{password}"
        token = base64.b64encode(cred.encode()).decode()
        headers['Authorization'] = f"Basic {token}"
        
        try:
            response = await client.get(url, headers=headers)
            
            # Handle GLPI Errors (400, 401, etc.)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"GLPI login failed: {response.text}"
                )

            data = response.json()
            return data.get("session_token")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()

    async def kill_session(
        self,
        session_token: str
    ) -> str:
        """
        Terminate a GLPI API session.
        
        Args:
            session_token: Valid session token from authentication.
        
        Returns:
            Bool of success.
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        url = f"{self.base_url}/killSession"
        
        try:
            response = await client.get(url, headers=self._get_headers(session_token))
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"GLPI failed to terminate session: {response.text}"
                )

            return True
        
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()
    
# Create a singleton instance to be imported elsewhere
auth_service = AuthService()