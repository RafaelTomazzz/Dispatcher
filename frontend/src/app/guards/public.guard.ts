import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const publicGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const token = localStorage.getItem('glpi_token');

  // If token exists, kick them to the queue
  if (token) {
    router.navigate(['/queue']);
    return false; // Block access to the login page
  }

  // If no token, allow access to login page
  return true;
};