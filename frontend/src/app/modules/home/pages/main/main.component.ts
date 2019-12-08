import { Component, OnInit } from '@angular/core';
import { faGraduationCap, faUniversity } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.sass']
})
export class MainComponent implements OnInit {

  faGraduationCap = faGraduationCap;
  faUniversity = faUniversity;
 // faAngleUp = faAngleUp;
 // faAngleUp = faAngleUp;
 // faAngleUp = faAngleUp;
 // faAngleUp = faAngleUp;
  
  constructor() { }

  ngOnInit() {
  }

}
