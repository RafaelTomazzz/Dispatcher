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
  private apiUrl = "http://localhost:8000/api/queue"

  getListQueue(): Observable<Ticket[]>{
    return this.http.get<any>(`${this.apiUrl}/fetchqueue?saved_search_id=164`).pipe(
      // map((ticketResponse) => {
      //   ticketResponse.queue_tickets.map()
      // })
      
      map((ticketResponse) => {
        return ticketResponse.queue_tickets.map((ticket:any) => ({
            id: ticket.id,
            entities_id: ticket.entities_id.split("PMC > ", 2).slice(1),
            name: ticket.name,
            urgency: ticket.urgency,
            locations_id: ticket.locations_id,
            date_creation: ticket.date_creation
          
        })) as Ticket[]
      })
    )
    
  }
}
