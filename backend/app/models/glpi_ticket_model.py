from pydantic import BaseModel

class TechAssign(BaseModel):
    """
    The data Angular sends to assign a technician to a ticket.
    """
    login: str
    ticket_id: int