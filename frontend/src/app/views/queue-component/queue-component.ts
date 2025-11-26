import { Component, OnInit, inject } from '@angular/core';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Ticket } from '../../models/ticketModel';
import { CommonModule } from '@angular/common';
import { TicketService } from '../../services/ticket.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-queue-component',
  imports: [CommonModule],
  templateUrl: './queue-component.html',
  styleUrl: './queue-component.css',
})

export class QueueComponent implements OnInit {

  tickets!: Ticket[]
  private router = inject(Router)

  @ViewChild('popup') popup!: ElementRef

  ngOnInit(): void {
    if(!localStorage.getItem('tickets') || this.activeRoute.snapshot.data['tickets'] != JSON.parse(localStorage.getItem('tickets') || '[]')){
      localStorage.setItem('tickets', JSON.stringify(this.activeRoute.snapshot.data['tickets']))
    }
    
    this.tickets = JSON.parse(localStorage.getItem('tickets') || '[]')
  }

  ngAfterViewInit(): void {
  }


  constructor(private ticketService: TicketService, private activeRoute: ActivatedRoute) { }

  ticketSelecionado!: number

  ShowHiddenPopUp() {
    try {
      if (!this.ticketSelecionado) {
        throw new Error
      }

      const ticket = this.tickets.filter(t => t.id === this.ticketSelecionado)

      localStorage.setItem('ticket', JSON.stringify(ticket))
      console.log(localStorage.getItem('ticket'))
      this.router.navigate(['/ticket']);
    } catch (error) {
      alert("Erro! Nenhum ticket selecionado")
    }
  }

  onChange(event: any){
    console.log(event.target.value)
    switch(event.target.value){
      case "infra":
        this.tickets = this.activeRoute.snapshot.data["ticketsInfra"]
        break
      case "externo":
        this.tickets = this.activeRoute.snapshot.data["ticketsExterno"]
        break
      default:
        this.tickets = this.activeRoute.snapshot.data["tickets"]
    }
  }
}