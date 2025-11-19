import { Component, OnInit } from '@angular/core';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Ticket } from '../../models/ticketModel';
import { UrgencyTypeEnum } from '../../enums/urgency-type-enum';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-queue-component',
  imports: [CommonModule],
  templateUrl: './queue-component.html',
  styleUrl: './queue-component.css',
})

export class QueueComponent implements OnInit{

  ngOnInit(): void {
      console.log(this.ticket1.id)
  }

  constructor() {}

  ticket1: Ticket = {
    id: 19824,
    name: "Devolução de micro",
    requesttype_id: "DRH",
    date_creation: new Date(2025, 10, 16),
    urgency: UrgencyTypeEnum.Alta
  }

  ticket2: Ticket = {
    id: 19990,
    name: "Micro não liga",
    requesttype_id: "UPA Sul",
    date_creation: new Date(2025, 10, 19),
    urgency: UrgencyTypeEnum.Media
  }

  ticket3: Ticket = {
    id: 19700,
    name: "Ponto de rede não funciona",
    requesttype_id: " SEDUC Sede",
    date_creation: new Date(2025, 10, 10),
    urgency: UrgencyTypeEnum.Baixa
  }

  ticket4: Ticket = {
    id: 19851,
    name: "A internet do prédio não funcionar",
    requesttype_id: "UBS Porto Novo",
    date_creation: new Date(2025, 10, 19),
    urgency: UrgencyTypeEnum.MuitoAlta
  }

    ticket5: Ticket = {
    id: 19698,
    name: "Micro de laboratória com lentidão",
    requesttype_id: "Emef Uijo",
    date_creation: new Date(2025, 10, 10),
    urgency: UrgencyTypeEnum.MuitoBaixa
  }

  tickets: Ticket[] = [this.ticket1, this.ticket2, this.ticket3, this.ticket4, this.ticket5]

  ticketSelecionado? : number
  
}
