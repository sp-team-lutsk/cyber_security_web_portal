import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { StudentsComponent } from './pages/students/students.component';
import { ScienceComponent } from './pages/science/science.component';
import { AboutComponent } from './pages/about/about.component';
import { MainComponent } from './pages/main/main.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';

const homeRoutes: Routes = [
  {path: '', component: MainComponent},
  {path: 'students', component: StudentsComponent},
  {path: 'science', component: ScienceComponent},
  {path: 'about', component: AboutComponent},
];

@NgModule({
  imports: [RouterModule.forChild(homeRoutes)],
  exports: [RouterModule]
})
export class HomeRoutingModule { }
