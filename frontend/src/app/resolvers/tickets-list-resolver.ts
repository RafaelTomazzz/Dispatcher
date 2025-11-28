import { ResolveFn } from '@angular/router';
import { Resolve } from '@angular/router';
import { Ticket } from '../models/ticketModel';
import { TicketService } from '../services/ticket.service';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class ticketsListInfraExterno implements Resolve<Ticket[]> {
  constructor(private ticketService: TicketService){}

  resolve(): Observable<Ticket[]>  {
    return this.ticketService.getListQueue(167)
  }
};
