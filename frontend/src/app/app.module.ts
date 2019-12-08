import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

<<<<<<< HEAD
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeModule } from './modules/home/home.module';
=======
import { AppComponent } from "./app.component";
import { HeaderComponent } from './main/header/header.component';
import { BodyComponent } from './main/body/body.component';
import { FooterComponent } from './footer/footer.component';
import { StudentsComponent } from "./students/students.component";
import { RouterModule } from "@angular/router";
import { ScienceComponent } from './science/science.component';
import { AboutComponent } from './about/about.component';
import { MailingComponent } from './mailing/mailing.component';

>>>>>>> master
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { DashboardModule } from './modules/dashboard/dashboard.module';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    HomeModule,
    BrowserModule,
<<<<<<< HEAD
    AppRoutingModule,
    FontAwesomeModule,
    DashboardModule,
=======
    RouterModule.forRoot(routes),
    FontAwesomeModule,
    BrowserAnimationsModule,
>>>>>>> master
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
