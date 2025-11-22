from pydantic import BaseModel

class UserCredentials(BaseModel):
    """
    The data Angular sends to log in.
    """
    login: str
    password: str