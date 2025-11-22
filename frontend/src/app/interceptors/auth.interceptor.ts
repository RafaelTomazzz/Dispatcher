import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router); // We can inject dependencies inside the function
  const token = localStorage.getItem('glpi_token');

  let requestToHandle = req;

  // 1. Add the header if token exists
  if (token) {
    requestToHandle = req.clone({
      headers: req.headers.set('x-glpi-session-token', token)
    });
  }

  // 2. Pass to next handler and listen for errors
  return next(requestToHandle).pipe(
    catchError((error: HttpErrorResponse) => {
      
      // 3. Handle 401 Unauthorized (Token expired/invalid)
      if (error.status === 401) {
        localStorage.removeItem('glpi_token');
        router.navigate(['/login']);
      }
      
      return throwError(() => error);
    })
  );
};