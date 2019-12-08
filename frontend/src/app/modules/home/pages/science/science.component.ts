import { Component, OnInit } from '@angular/core';
import { faAngleDown, faAngleUp, faChartLine, faEdit } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-science',
  templateUrl: './science.component.html',
  styleUrls: ['./science.component.sass']
})
export class ScienceComponent implements OnInit {

  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;
  faChartLine = faChartLine;
  faEdit = faEdit;

  constructor() { }

  ngOnInit() {
  }

}
