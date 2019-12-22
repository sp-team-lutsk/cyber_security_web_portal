import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminComponent } from './admin/admin.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ModeratorComponent } from './moderator/moderator.component';

@NgModule({
  declarations: [AdminComponent, ModeratorComponent],
  imports: [
 	FontAwesomeModule,
    CommonModule,
    DashboardRoutingModule,
  ]
  
})
export class DashboardModule { }
