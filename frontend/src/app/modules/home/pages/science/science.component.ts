import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp } from '@fortawesome/fontawesome-free';

@Component({
  selector: 'app-science',
  templateUrl: './science.component.html',
  styleUrls: ['./science.component.sass']
})
export class ScienceComponent implements OnInit {

  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;
  constructor() { }

  ngOnInit() {
  }

}
