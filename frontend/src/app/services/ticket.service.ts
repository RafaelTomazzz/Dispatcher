import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ticket } from '../models/ticketModel';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TicketService {
  private http = inject(HttpClient)
  private apiUrl = "http://localhost:8000/api/"

  getListQueue(id:number): Observable<Ticket[]>{
    return this.http.get<any>(`${this.apiUrl}queue/fetchqueue?saved_search_id=${id}`).pipe(
      map((ticketResponse) => {
        return ticketResponse.queue_tickets.map((ticket:any) => ({
            id: ticket.id,
            entities_id: ticket.entities_id.split("PMC > ").slice(1),
            name: ticket.name,
            urgency: ticket.urgency,
            locations_id: ticket.locations_id,
            date_creation: ticket.date_creation
          
        })) as Ticket[]
      })
    )    
  }
  
  postTicketAssingSelf(ticket_id: number): Observable<any>{
    return this.http.post<any>(`${this.apiUrl}ticket/assignself`, {
      user_id: localStorage.getItem('glpi_user'),
      ticket_id: ticket_id
    })
  }
}

