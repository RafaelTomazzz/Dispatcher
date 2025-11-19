import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-pop-up-component',
  imports: [RouterLink],
  templateUrl: './pop-up-component.html',
  styleUrl: './pop-up-component.css',
})
export class PopUpComponent {
  Reload(){
    location.reload()
  }
}
