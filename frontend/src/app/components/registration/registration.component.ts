import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  @Output() close = new EventEmitter();
  constructor() { }

  ngOnInit() {
  }

}