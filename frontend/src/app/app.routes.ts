import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { publicGuard } from './guards/public.guard';

import { LoginComponent } from './views/login-component/login-component';
import { QueueComponent } from './views/queue-component/queue-component';
import { TicketComponent } from './views/ticket-component/ticket-component';
import { ticketsListInfraExterno } from './resolvers/tickets-list-resolver';
import { ticketListinfra } from './resolvers/ticket-list-infra-resolver';
import { ticketsListExterno } from './resolvers/ticket-list-externo-resolver';

export const routes: Routes = [
    {
        path: "",
        redirectTo: 'login',
        pathMatch: 'full'
    },
    {
        path: 'login',
        loadComponent: () => import('./views/login-component/login-component').then(m => m.LoginComponent),
        canActivate: [publicGuard]
    },
    {
        path: "queue",
        loadComponent: () => import('./views/queue-component/queue-component').then(m => m.QueueComponent),
        resolve: {
            tickets: ticketsListInfraExterno,
            ticketsInfra: ticketListinfra,
            ticketsExterno: ticketsListExterno
        },
        canActivate: [authGuard]
    },
    {
        path: "ticket",
        loadComponent: () => import('./views/ticket-component/ticket-component').then(m => m.TicketComponent),
        canActivate: [authGuard]
    }
];