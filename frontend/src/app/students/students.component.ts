import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.css']
})

export class StudentsComponent implements OnInit {
  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;

  constructor() { }

  ngOnInit() {
  }

}
