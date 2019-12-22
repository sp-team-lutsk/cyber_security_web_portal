import { Component, OnInit } from '@angular/core';
import { faAngleLeft, faAngleDown, faSearch, faCog, faBell, faSignOutAlt, faBlog, faEllipsisH, faTimes} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-moderator',
  templateUrl: './moderator.component.html',
  styleUrls: ['./moderator.component.sass']
})
export class ModeratorComponent implements OnInit {

	faAngleLeft = faAngleLeft;
	faAngleDown = faAngleDown;
	faSearch = faSearch;
	faCog = faCog;
	faBell = faBell;
	faSignOutAlt = faSignOutAlt;
	faBlog = faBlog;
	faEllipsisH = faEllipsisH;
	faTimes = faTimes;

  constructor() { }

  ngOnInit() {
  }

}
