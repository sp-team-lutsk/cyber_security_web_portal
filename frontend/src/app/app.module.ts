import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from "./app.component";
import { HeaderComponent } from './main/header/header.component';
import { BodyComponent } from './main/body/body.component';
import { FooterComponent } from './footer/footer.component';
import { StudentsComponent } from "./students/students.component";
import { RouterModule } from "@angular/router";
import { ScienceComponent } from './science/science.component';
import { StructureComponent } from './structure/structure.component';
import { AboutComponent } from './about/about.component';

const routes = [
  {path: '', component: BodyComponent},
  {path: 'students', component: StudentsComponent},
  {path: 'science', component: ScienceComponent},
  {path: 'structure', component: StructureComponent},
  {path: 'about', component: AboutComponent},
]

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    BodyComponent,
    StudentsComponent,
    FooterComponent,
    ScienceComponent,
    StructureComponent,
    AboutComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [
    AppComponent,
    HeaderComponent,
    BodyComponent,
    StudentsComponent,
    ScienceComponent,
    StructureComponent,
    AboutComponent,
    FooterComponent,
  ],
})

export class AppModule { }
