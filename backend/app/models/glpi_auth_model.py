from pydantic import BaseModel

class UserCredentials(BaseModel):
    """
    The data Angular sends to log in.
    We use a personal user_token (generated in GLPI settings) 
    as it is safer and easier than storing username/passwords.
    """
    login: str
    password: str

class TokenResponse(BaseModel):
    """
    What we send back to Angular.
    """
    session_token: str