import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = 'http://localhost:8000/api/auth';

  login(credentials: any) {
    return this.http.post<any>(`${this.apiUrl}/login`, credentials).pipe(
      tap(response => {
        if (response.session_token) {
          // Store the token
          localStorage.setItem('glpi_token', 'n96se0tv0seq4945v32eo2hfrr');
          localStorage.setItem('glpi_user', response.username);
        }
      })
    );
  }

  logout() {
    this.http.post(`${this.apiUrl}/logout`, {}).subscribe({
      next: () => console.log('Session killed on server'),
      error: (err) => console.warn('Could not kill server session', err)
    })

    // Clear local state immediately (don't wait for server response)
    localStorage.removeItem('glpi_token');
    localStorage.removeItem('glpi_user');
    this.router.navigate(['/login']);
  }
}