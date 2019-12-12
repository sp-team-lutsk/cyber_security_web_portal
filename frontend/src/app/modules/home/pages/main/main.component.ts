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
