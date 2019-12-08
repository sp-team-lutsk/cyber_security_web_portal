import { Component, OnInit } from '@angular/core';
import { faUserGraduate, faAtom, faPencilRuler, faBlog, faQuestion } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.sass']
})
export class FooterComponent implements OnInit {

  faUserGraduate = faUserGraduate;
  faAtom = faAtom;
  faPencilRuler = faPencilRuler;
  faBlog = faBlog;
  faQuestion = faQuestion;



  constructor() { }

  ngOnInit() {
  }

}
