import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from "./app.component";
import { HeaderComponent } from './main/header/header.component';
import { BodyComponent } from './main/body/body.component';
import { FooterComponent } from './footer/footer.component';
import { StudentsComponent } from "./students/students.component";
import { RouterModule } from "@angular/router";
import { ScienceComponent } from './science/science.component';
import { AboutComponent } from './about/about.component';
import { MailingComponent } from './mailing/mailing.component';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RegistrationComponent } from './components/registration/registration.component';
import { LogInComponent } from './components/log-in/log-in.component';

const routes = [
      {path: '', component: BodyComponent},
      {path: 'students', component: StudentsComponent},
      {path: 'science', component: ScienceComponent},
      {path: 'about', component: AboutComponent},
      {path: 'mailing', component: MailingComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    BodyComponent,
    StudentsComponent,
    FooterComponent,
    ScienceComponent,
    AboutComponent,
    MailingComponent,
    RegistrationComponent,
    LogInComponent,

  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    FontAwesomeModule,
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [
    AppComponent,
    HeaderComponent,
    BodyComponent,
    StudentsComponent,
    ScienceComponent,
    AboutComponent,
    MailingComponent,
    FooterComponent,
  ],
})

export class AppModule { }
