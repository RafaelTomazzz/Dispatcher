import { Component, OnInit } from '@angular/core';
import { Ticket } from '../../models/ticketModel';
import { RouterLink } from '@angular/router';
import { DatePipe } from '@angular/common';
import { CommonModule } from '@angular/common';
import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';


@Component({
  standalone: true,
  selector: 'app-ticket-component',
  imports: [RouterLink, CommonModule, DatePipe],
  templateUrl: './ticket-component.html',
  styleUrl: './ticket-component.css',
})
export class TicketComponent implements OnInit {

  tickets: Ticket[] = JSON.parse(localStorage.getItem('ticket') || "[]")
  ticket: Ticket = this.tickets[0]

  @ViewChild("timer") timer! : ElementRef

  interval: any
  segundos = 0
  tempoFormatado: string = "00:00:00"
  showTimer: boolean = false;

  ngOnInit(): void {

  }

  timerStart() {
    this.showTimer = true;
    this.interval = setInterval(() => {
      this.segundos++
      this.tempoFormatado = this.formatarTempo(this.segundos)
    }, 1000)

    this.timer.nativeElement.innerHTML = "{{tempoFormatado}}"

  }

  private formatarTempo(seg: number): string {
    const horas = Math.floor(seg / 3600);
    const minutos = Math.floor((seg % 3600) / 60);
    const segundos = seg % 60;

    return [
      String(horas).padStart(2, '0'),
      String(minutos).padStart(2, '0'),
      String(segundos).padStart(2, '0')
    ].join(':');
  }

  timerStop() {
    clearInterval(this.interval)
  }
}
