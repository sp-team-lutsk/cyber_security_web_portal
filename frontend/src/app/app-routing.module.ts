import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StudentsComponent } from './modules/home/pages/students/students.component';
import { ScienceComponent } from './modules/home/pages/science/science.component';
import { AboutComponent } from './modules/home/pages/about/about.component';
import { MainComponent } from './modules/home/pages/main/main.component';
import { HeaderComponent } from './modules/home/components/header/header.component';
import { FooterComponent } from './modules/home/components/footer/footer.component';

const routes: Routes = [
  {path: 'footer', component: FooterComponent},
  {path: 'header', component: HeaderComponent},
  {path: 'main', component: MainComponent},
  {path: 'students', component: StudentsComponent},
  {path: 'science', component: ScienceComponent},
  {path: 'about', component: AboutComponent},
];

@NgModule({
  imports: [],
  exports: [RouterModule]
})
export class AppRoutingModule { }
