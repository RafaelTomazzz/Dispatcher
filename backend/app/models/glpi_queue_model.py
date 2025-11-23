from pydantic import BaseModel

class Queue(BaseModel):
    """
    The data Angular sends to execute a search.
    """
    saved_search_id: int