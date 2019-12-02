import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminComponent } from './admin/admin.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@NgModule({
  declarations: [AdminComponent],
  imports: [
 	FontAwesomeModule,
    CommonModule,
    DashboardRoutingModule,
  ]
})
export class DashboardModule { }
