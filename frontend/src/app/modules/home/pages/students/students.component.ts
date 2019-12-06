import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp, faNewspaper, faGraduationCap, faEdit, faChalkboardTeacher, faBlog } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.sass']
})
export class StudentsComponent implements OnInit {
  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;
  faNewspaper = faNewspaper;
  faGraduationCap = faGraduationCap;
  faEdit = faEdit;
  faChalkboardTeacher = faChalkboardTeacher;
  faBlog = faBlog;

  constructor() { }

  ngOnInit() {
  }

}
