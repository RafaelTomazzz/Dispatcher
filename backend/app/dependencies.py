from fastapi import Header, HTTPException

async def get_glpi_token(x_glpi_session_token: str = Header(...)):
    if not x_glpi_session_token:
        raise HTTPException(status_code=401, detail="GLPI Session Token missing")
    return x_glpi_session_token