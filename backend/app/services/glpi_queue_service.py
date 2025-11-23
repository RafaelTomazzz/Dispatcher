import httpx
from urllib.parse import urlencode
from fastapi import HTTPException
from typing import Optional, Union, List, Dict, Any, Tuple
from .base_service import GLPIBaseService

class QueueService(GLPIBaseService):
    
    async def get_saved_search_results(
        self,
        session_token: str,
        savedsearch_id: int,
        expand_dropdowns: bool = False,
        range_param: str = "0-49"
    ) -> dict:
        """
        Fetch results from a GLPI saved search by ID.
        
        This function retrieves the saved search definition, extracts its itemtype and query parameters,
        then executes a search with those parameters.
        
        Args:
            session_token: Valid session token from authentication.
            savedsearch_id: ID of the saved search.
            expand_dropdowns: Whether to expand dropdown fields to names (default: False).
            range_param: Pagination range (default: '0-49').
        
        Returns:
            Dict of search_results.
        """
        
        ### Retrieving saved search itemtype and query parameters
        
        client = await self.get_async_client() # user, password params if using proxy
        saved_search_url = f"{self.base_url}/SavedSearch/{savedsearch_id}"
        
        try:
            saved_search_response = await client.get(saved_search_url, headers=self._get_headers(session_token))
            
            if saved_search_response.status_code != 200:
                raise HTTPException(
                    status_code=saved_search_response.status_code, 
                    detail=f"GLPI failed to fetch saved search item: {saved_search_response.text}"
                )
            
            saved_search_data = saved_search_response.json()
            itemtype = saved_search_data.get('itemtype')
            query_str = saved_search_data.get('query', '')
            
            if not itemtype:
                return None
        
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        
        ### Executing search with acquired parameters
        
        search_url = f"{self.base_url}/search/{itemtype}"
    
        additional_params = {
            'expand_dropdowns': str(expand_dropdowns).lower(),
            'range': range_param,
        }
        full_query_str = f"{query_str}&{urlencode(additional_params)}".lstrip('&')
        
        try:
            search_response = await client.get(f"{search_url}?{full_query_str}", headers=self._get_headers(session_token))
            
            if search_response.status_code != 200:
                raise HTTPException(
                    status_code=search_response.status_code, 
                    detail=f"GLPI failed to fetch search items: {search_response.text}"
                )
            
            search_data = search_response.json()
            return search_data
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()
            
    async def get_ticket_data(
        self,
        session_token: str,
        search_data: Optional[Dict[str, Any]] = None,
        ticket_ids: Optional[Union[int, List[int]]] = None,
        expand_dropdowns: bool = True,
    ) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Retrieve full details for tickets from GLPI search results or specified IDs.
        
        Args:
            session_token: Valid session token from authentication.
            search_data: Optional Dict from search results (e.g., from get_saved_search_results).
                        If provided, extracts ticket IDs from 'data' rows using key '2'.
            ticket_ids: Optional single int or List[int] of ticket IDs to fetch.
                        If provided, uses these directly (converts single int to list).
            expand_dropdowns: Whether to expand dropdown fields (default: True).
        
        Returns:
          List of dicts tickets_list. Each item in tickets_list is the full ticket dict from GLPI.
        
        Notes:
            - Provide either search_data or ticket_ids, but not both (prioritizes ticket_ids if both given).
            - If neither is provided, returns empty list (no error).
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        
        ### Determine ticket_ids
        
        if ticket_ids is not None:
            if isinstance(ticket_ids, int):
                ticket_ids_list = [ticket_ids]
            else:
                ticket_ids_list = list(ticket_ids)
        elif search_data is not None:
            data_rows = search_data.get('data', [])
            ticket_ids_list = []
            for row in data_rows:
                tid = row.get('2')  # Search option 2 is the ID
                if tid:
                    ticket_ids_list.append(int(tid))
        else:
            return []  # No source provided, return empty
        
        if not ticket_ids_list:
            return None
        
        ### Retrieving each ticket's data
        
        additional_params = {
            'expand_dropdowns': str(expand_dropdowns).lower()
        }
        full_query_str = urlencode(additional_params)
        
        tickets = []
            
        try:
            for tid in ticket_ids_list:
                ticket_url = f"{self.base_url}/Ticket/{tid}?{full_query_str}"
                ticket_data_search = await client.get(ticket_url, headers=self._get_headers(session_token))
            
                if ticket_data_search.status_code != 200:
                    raise HTTPException(
                        status_code=ticket_data_search.status_code, 
                        detail=f"GLPI failed to fetch ticket {tid} data: {ticket_data_search.text}"
                    )
                    continue
                
                ticket_data = ticket_data_search.json()
                tickets.append(ticket_data)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()
        
        if not tickets:
            return None
        return tickets