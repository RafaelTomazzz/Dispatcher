import { Component } from '@angular/core';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Ticket } from '../../models/ticketModel'; 
import { UrgencyTypeEnum } from '../../enums/urgency-type-enum';

@Component({
  standalone: true,
  selector: 'app-queue-component',
  imports: [ ],
  templateUrl: './queue-component.html',
  styleUrl: './queue-component.css',
})
export class QueueComponent {
  
  tikcet1 : Ticket = {
    id: 1,
    name: "Devolução de micro",
    requesttype_id: "SESAU",
    date_creation: new Date(2025, 0, 15),
    urgency: UrgencyTypeEnum.Alta
  }
  
}
