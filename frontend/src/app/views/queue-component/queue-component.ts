import { Component, OnInit, inject } from '@angular/core';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Ticket } from '../../models/ticketModel';
import { CommonModule } from '@angular/common';
import { TicketService } from '../../services/ticket.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { tick } from '@angular/core/testing';

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

  lastTeam : string = ''

  teamChange(event: any){
    const currentTeam = !event.target.value ? this.lastTeam : event.target.value
    this.lastTeam = currentTeam

    switch(currentTeam){
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

  dataBoolean: boolean = false

  dataFilter($event: any){
    switch(this.dataBoolean){
      case false:
        this.dataBoolean = true
        this.tickets.sort((ticketA, ticketB) => 
          new Date(ticketA.date_creation).getTime() - new Date(ticketB.date_creation).getTime()
        )
        break
      case true:
        this.dataBoolean = false
        this.teamChange($event)
    }
  }
}