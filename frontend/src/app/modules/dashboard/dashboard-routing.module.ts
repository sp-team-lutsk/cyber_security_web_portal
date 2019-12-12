import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AdminComponent } from './admin/admin.component';
import { ModeratorComponent } from './moderator/moderator.component';


const dashboardRoutes: Routes = [
  {path: 'admin', component: AdminComponent},
  {path: 'moderator', component: ModeratorComponent},
];

@NgModule({
  imports: [RouterModule.forChild(dashboardRoutes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule { }
