from fastapi import APIRouter, Depends, HTTPException
from app.services.glpi_queue_service import QueueService
from app.dependencies import get_glpi_token

router = APIRouter()

@router.get("/fetchqueue")
async def get_queue_data(saved_search_id: int, session_token: str = Depends(get_glpi_token)):
    """
    Endpoint to retrieve a team's current ticket's queue.
    Receives a GLPI SavedSearch ID, talks to GLPI, and returns a list of dicts with each retrieved ticket info.
    URL will look like: /api/queue/fetchqueue?saved_search_id=123
    """
    
    saved_search_results = await QueueService().get_saved_search_results(session_token, saved_search_id)
    
    if not saved_search_results:
        raise HTTPException(status_code=401, detail="Queue search failed")
    
    queue_tickets = await QueueService().get_ticket_data(session_token, search_data = saved_search_results)
    
    if not queue_tickets:
        raise HTTPException(status_code=401, detail="Retrieval of Queue tickets failed")
    
    return {
        "message": "Fetch Queue successful",
        "queue_tickets": queue_tickets
    }