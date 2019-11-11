import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-science',
  templateUrl: './science.component.html',
  styleUrls: ['./science.component.css']
})
export class ScienceComponent implements OnInit {
  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;

  constructor() { }

  ngOnInit() {
  }

}
