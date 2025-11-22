import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

import { LoginComponent } from './views/login-component/login-component';
import { QueueComponent } from './views/queue-component/queue-component';
import { TicketComponent } from './views/ticket-component/ticket-component';

export const routes: Routes = [
    {
        path: "",
        redirectTo: 'login',
        pathMatch: 'full'
    },
    {
        path: 'login',
        loadComponent: () => import('./views/login-component/login-component').then(m => m.LoginComponent)
    },
    {
        path: "queue",
        loadComponent: () => import('./views/queue-component/queue-component').then(m => m.QueueComponent),
        canActivate: [authGuard]
    },
    {
        path: "ticket",
        loadComponent: () => import('./views/ticket-component/ticket-component').then(m => m.TicketComponent),
        canActivate: [authGuard]
    }
];