from fastapi import APIRouter, Depends, HTTPException
from app.models.glpi_ticket_model import TechAssign
from app.services.glpi_ticket_service import TicketService
from app.dependencies import get_glpi_token

router = APIRouter()

@router.get("/fetchsubitem")
async def get_subitem_data(ticket_id: int, subitem_type: str, session_token: str = Depends(get_glpi_token)):
    """
    Endpoint to retrieve a ticket's subitem data.
    Receives a GLPI ticket ID and subitem type, talks to GLPI, and returns a list of dicts with each retrieved subitem info.
    URL will look like: /api/ticket/fetchsubitem?ticket_id=123&subitem_type:Ticket_User
    """
    
    subitem_data = await TicketService().get_ticket_subitems(session_token, ticket_id, subitem_type)
    
    if not subitem_data:
        raise HTTPException(status_code=401, detail="Subitem search failed")
    
    return {
        "message": "Fetch subitem successful",
        "subitem_data": subitem_data
    }

@router.post("/assignself")
async def assign_to_ticket(AssignData: TechAssign, session_token: str = Depends(get_glpi_token)):
    """
    Endpoint to assign the user to a ticket.
    Receives a GLPI ticket ID and login, talks to GLPI, checks for any previously assigned actors, and returns a bool of success.
    """
    ### Fetch current assigned users
    ticket_users = await TicketService().get_ticket_subitems(session_token, AssignData.ticket_id, "Ticket_User")
    
    previously_assigned_technicians = []
    for actor in ticket_users:
        if actor.get("type") == 2:
            previously_assigned_technicians.append(actor.get("users_id"))
    
    ### Remove current assigned users        
    remove_assigned_technicians = await TicketService().remove_existing_assigned_techs(session_token, AssignData.ticket_id, ticket_users)
    
    if not remove_assigned_technicians:
        raise HTTPException(status_code=401, detail="Assigned actors deletion failed")
    
    ### Assign user to ticket
    assign_technician = await TicketService().assign_technician(session_token, AssignData.ticket_id, AssignData.user_id)
    
    if not assign_technician:
        raise HTTPException(status_code=401, detail="Failed to assign user to ticket")
    
    ### Update ticket status to Em Atendimento
    updated_ticket_data = {
        'status': 2
    }
    
    update_status = await TicketService().update_ticket(session_token, AssignData.ticket_id, updated_ticket_data)
    
    if not update_status:
        raise HTTPException(status_code=401, detail="Failed to update ticket status")
    
    return {
        "message": "Technician assign successful",
        "user_assigned": assign_technician,
        "status_updated": update_status,
        "previously_assigned_technicians": previously_assigned_technicians,
        "deleted_count": remove_assigned_technicians["deleted"],
        "errors": remove_assigned_technicians["errors"]
    }