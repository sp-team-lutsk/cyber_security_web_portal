import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp } from '@fortawesome/fontawesome-free';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.sass']
})
export class StudentsComponent implements OnInit {
  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;

  constructor() { }

  ngOnInit() {
  }

}
