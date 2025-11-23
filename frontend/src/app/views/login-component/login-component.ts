import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms'; // <--- Crucial Import
import { AuthService } from '../../services/auth.service'; // Adjust path if needed

@Component({
  selector: 'app-login-component',
  standalone: true,
  imports: [FormsModule], // <--- Add FormsModule here
  templateUrl: './login-component.html',
  styleUrl: './login-component.css',
})
export class LoginComponent {
  
  // Inject dependencies
  private authService = inject(AuthService);
  private router = inject(Router);

  // Variables bound to the HTML
  username = '';
  password = '';
  errorMessage = '';
  isLoading = false;

  Submit() {
    // Basic validation
    if (!this.username || !this.password) {
      this.errorMessage = '> informe usuário e senha <';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const credentials = { 
      login: this.username, 
      password: this.password 
    };

    this.authService.login(credentials).subscribe({
      next: () => {
        // On success, navigate to queue
        this.isLoading = false;
        this.router.navigate(['/queue']);
      },
      error: (err) => {
        // On error, show message and stop loading
        console.error(err);
        this.isLoading = false;
        this.errorMessage = '> login ou senha inválidos <';
      }
    });
  }
}