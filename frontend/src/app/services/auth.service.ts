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
          localStorage.setItem('glpi_token', response.session_token);
          localStorage.setItem('glpi_user', response.username);
        }
      })
    );
  }

  logout() {
    // Add kill_session call
    const token = localStorage.getItem('glpi_token');

    const kill_session = this.http.post<any>(`${this.apiUrl}/logout`, token)

    // Don't wait for the result, just clear local state
    localStorage.removeItem('glpi_token');
    localStorage.removeItem('glpi_user');
    this.router.navigate(['/login']);
  }
}