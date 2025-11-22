from fastapi import APIRouter, Depends, HTTPException
from app.models.glpi_auth_model import UserCredentials
from app.services.glpi_auth_service import AuthService
from app.dependencies import get_glpi_token

router = APIRouter()

@router.post("/login")
async def login(credentials: UserCredentials):
    """
    Endpoint to authenticate a user.
    Receives user and password, talks to GLPI, and returns session_token.
    """
    session_token = await AuthService().init_session(credentials.login, credentials.password)
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Authentication failed")
        
    return {
        "message": "Login successful",
        "session_token": session_token,
        "username": credentials.login 
    }

@router.post("/logout")
async def logout(session_token: str = Depends(get_glpi_token)):
    """
    Endpoint to logout a user.
    Receives session_token from LocalStorage, talks to GLPI, and returns success bool.
    """
    logout_sucess = await AuthService().kill_session(session_token)
    
    if not logout_sucess:
        raise HTTPException(status_code=401, detail="Logout failed")
    
    return {
        "message": "Logout successful",
        "session_token": session_token,
        "success": True
    }