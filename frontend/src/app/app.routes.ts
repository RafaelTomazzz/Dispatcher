import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';
import { publicGuard } from './guards/public.guard';

import { LoginComponent } from './views/login-component/login-component';
import { QueueComponent } from './views/queue-component/queue-component';
import { TicketComponent } from './views/ticket-component/ticket-component';
import { ticketsListResolveResolver } from './resolvers/tickets-list-resolve-resolver';

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
            tickets: ticketsListResolveResolver
        },
        canActivate: [authGuard]
    },
    {
        path: "ticket",
        loadComponent: () => import('./views/ticket-component/ticket-component').then(m => m.TicketComponent),
        canActivate: [authGuard]
    }
];