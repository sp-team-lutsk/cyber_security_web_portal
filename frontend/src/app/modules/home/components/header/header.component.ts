import { Component, OnInit } from '@angular/core';
import { faUniversity } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.sass']
})
export class HeaderComponent implements OnInit {

  faUniversity = faUniversity;

  constructor() { }

  ngOnInit() {
  }

}
