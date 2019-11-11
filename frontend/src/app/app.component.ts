import { Component } from '@angular/core';

import { faAngleDown, faAngleUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;
  title = 'frontend';
}
