import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Route } from '@angular/router';
import { Observable } from 'rxjs';
import { Ticket } from '../models/ticketModel';

@Injectable({
  providedIn: 'root',
})
export class TicketService {
  private http = inject(HttpClient)
  private apiUrl = "http://192.168.11.235:8000/api/queue"

  getListQueue(): Observable<Ticket[]>{
    return this.http.get<Ticket[]>(`${this.apiUrl}/fetchqueue?saved_search_id=164`)
  }
}
