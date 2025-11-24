import httpx
from fastapi import HTTPException
from typing import List, Dict, Tuple, Any
from .base_service import GLPIBaseService

class TicketService(GLPIBaseService):
    
    async def get_ticket_subitems(
        self,
        session_token: str,
        ticket_id: int,
        subitem_type: str,
        expand_dropdowns: bool = True,
        range_param: str = '0-49'
    ) -> List[Dict[str, Any]]:
        """
        Retrieve sub-items data for a specific ticket.
        
        Args:
            session_token: Valid session token from authentication.
            ticket_id: ID of the ticket.
            sub_itemtype: The sub-item type (e.g., ITILFollowup, ITILSolution, Item_Ticket, Ticket_User, Group_Ticket).
            range_param: Pagination range (default: '0-49').
        
        Returns:
            List of dicts subitems_list.
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        ticket_subitem_url = f"{self.base_url}/Ticket/{ticket_id}/{subitem_type}"
        
        params = {'range': range_param} if range_param else {}
        if expand_dropdowns:
            params['expand_dropdowns'] = str(expand_dropdowns).lower()
        
        try:
            subitem_search = await client.get(f"{ticket_subitem_url}", headers=self._get_headers(session_token), params=params)
            
            if subitem_search.status_code != 200:
                raise HTTPException(
                    status_code=subitem_search.status_code, 
                    detail=f"GLPI failed to fetch subitem data: {subitem_search.text}"
                )
            
            subitem_data = subitem_search.json()
            return subitem_data
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()
    
    async def remove_existing_assigned_techs(
        self,
        session_token: str,
        ticket_id: int,
        subitems: list,
    ) -> Tuple[bool, int, list[str]]:
        """
        Remove all existing technician assignments (type=2) from a ticket's Ticket_User subitems.
        Ensures only one technician can be assigned afterward.
        
        Args:
            session_token: Valid session token from authentication.
            ticket_id: ID of the ticket.
            sub_items: The list to check against, returned from get_ticket_subitems.
        
        Returns:
            Dict of bool for success, int for technicians deleted, list of str for registered errors. Success is True if all deletions succeeded or no assignments found.
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        ticket_subitem_url = f"{self.base_url}/Ticket/{ticket_id}/Ticket_User"
        
        if not subitems:
            return True
        
        deleted_count = 0
        errors = []
        
        async with await self.get_async_client() as client:
            for item in subitems:
                if item.get("type") != 2:
                    continue

                sub_id = item.get("id")
                if not isinstance(sub_id, int):
                    errors.append(f"Invalid sub-item ID: {sub_id!r}")
                    continue

                delete_url = f"{ticket_subitem_url}/{sub_id}"

                try:
                    resp = await client.delete(delete_url, headers=self._get_headers(session_token))
                except httpx.RequestError as exc:
                    errors.append(f"Network error deleting subitem {sub_id}: {exc}")
                    continue

                if resp.status_code != 200:
                    errors.append(f"Failed to delete subitem {sub_id}: {resp.status_code} {resp.text}")
                    continue

                deleted_count += 1

        return {"success": True, "deleted": deleted_count, "errors": errors}
    
    async def assign_technician(
        self,
        session_token: str,
        ticket_id: int,
        user_id: int,
        use_notification: int = 1
    ) -> bool:
        """
        Assign a technician to a ticket by adding a Ticket_User subitem with type=2 (assigned).
        
        Args:
            session_token: Valid session token from authentication.
            ticket_id: ID of the ticket.
            technician_user_id: ID of the user (technician) to assign.
            use_notification: Whether to send notifications (default: 1).
        
        Returns:
            Bool of success. success is False on failure.
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        ticket_subitem_url = f"{self.base_url}/Ticket/{ticket_id}/Ticket_User"
        
        payload = {
            "input": {
                "tickets_id": ticket_id,
                "users_id": user_id,
                "type": 2,
                "use_notification": use_notification
            }
        }
        
        try:
            assign_user = await client.post(f"{ticket_subitem_url}", headers=self._get_headers(session_token), json=payload)
            
            if assign_user.status_code != 201:
                raise HTTPException(
                    status_code=assign_user.status_code, 
                    detail=f"GLPI failed to add user to assigned: {assign_user.text}"
                )
            
            response = assign_user.json()
            if 'id' in response:
                return True
            else:
             return False
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()
            
    async def update_ticket(
        self,
        session_token: str,
        ticket_id: int,
        new_input = dict
    ) -> bool:
        """
        Update a GLPI ticket; specifically its status (e.g., from 3 to 2).
        
        Args:
            session_token: Valid session token from authentication.
            ticket_id: ID of the ticket.
            new_input: New status value (integer, e.g., 1 for 'New', 2 for 'Assigned').
        
        Returns:
            Bool of Success. Success is False on failure.
        """
        
        client = await self.get_async_client() # user, password params if using proxy
        ticket_url = f"{self.base_url}/Ticket/{ticket_id}"
        
        payload = {
            "input": new_input
        }
        
        try:
            update_ticket = await client.put(f"{ticket_url}", headers=self._get_headers(session_token), json=payload)
            
            if update_ticket.status_code != 200:
                raise HTTPException(
                    status_code=update_ticket.status_code, 
                    detail=f"GLPI failed to update ticket {ticket_id}: {update_ticket.text}"
                )
            
            response = update_ticket.json()
            if str(ticket_id) in response[0].keys():
                return True
            else:
                return False
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Unable to connect to GLPI: {str(exc)}")
        finally:
            await client.aclose()