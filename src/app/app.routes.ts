import { Routes } from '@angular/router';
import { LoginComponent } from './views/login-component/login-component';
import { QueueComponent } from './views/queue-component/queue-component';

export const routes: Routes = [
    {
        path: "",
        component: LoginComponent
    },
    {
        path: "queue",
        component: QueueComponent
    }
];
