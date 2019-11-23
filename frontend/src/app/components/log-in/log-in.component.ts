import {Component, EventEmitter, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent implements OnInit {
  @Output() close = new EventEmitter();
  constructor() { }

  ngOnInit() {
  }

}
