import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: [
    './header.component.css'
  ]

})
export class HeaderComponent implements OnInit {
  public showRegistration = false;
  public showLogin = false;

  constructor() { }

  ngOnInit() {

  }
  toggle(){
    this.showRegistration = !this.showRegistration;
    console.log(this.showRegistration);
  }
  closeRegistration(event) {
    this.showRegistration = event;
  }

  toggle1(){
    this.showLogin = !this.showLogin;
    console.log(this.showLogin);
  }
  closeLogin(event) {
    this.showLogin = event;
  }
}
