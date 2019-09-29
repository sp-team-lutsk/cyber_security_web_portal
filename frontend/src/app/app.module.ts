import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';

import { AlertModule, ButtonsModule } from 'ngx-bootstrap';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { BodyComponent } from './body/body.component';

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    BodyComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AlertModule.forRoot(),
    ButtonsModule.forRoot(),
  ],
  providers: [],
  bootstrap: [
    HeaderComponent,
    FooterComponent,
    BodyComponent
  ],
})

export class AppModule { }
