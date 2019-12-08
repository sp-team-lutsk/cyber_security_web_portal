import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeModule } from './modules/home/home.module';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DashboardModule } from './modules/dashboard/dashboard.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    HomeModule,
    BrowserModule,

    AppRoutingModule,
    FontAwesomeModule,
    DashboardModule,

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
