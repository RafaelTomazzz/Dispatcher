from fastapi import APIRouter, HTTPException
from app.models.glpi_auth_model import UserCredentials, TokenResponse
from app.services.glpi_auth_service import glpi_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse)

async def login(credentials: UserCredentials):
    """
    Endpoint to authenticate a user.
    Receives a user_token, talks to GLPI, and returns a session_token.
    """
    session_token = await glpi_service.init_session(credentials.login, credentials.password)
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Authentication failed")
        
    return TokenResponse(session_token=session_token)