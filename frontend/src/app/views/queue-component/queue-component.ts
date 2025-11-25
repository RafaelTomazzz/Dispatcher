import { Component, OnInit, inject } from '@angular/core';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Ticket } from '../../models/ticketModel';
import { CommonModule } from '@angular/common';
import { TicketService } from '../../services/ticket.service';
import { Router } from '@angular/router';

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

  }

  ngAfterViewInit(): void {
    this.ticketService.getListQueue().subscribe(res => {
      this.tickets = res

      console.log(res)
    })

    console.log(this.tickets)
  }


  constructor(private ticketService: TicketService) { }

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
}