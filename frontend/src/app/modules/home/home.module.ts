import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { StudentsComponent } from './pages/students/students.component';
import { ScienceComponent } from './pages/science/science.component';
import { AboutComponent } from './pages/about/about.component';
import { MainComponent } from './pages/main/main.component';



@NgModule({
  declarations: [HeaderComponent, FooterComponent, StudentsComponent, ScienceComponent, AboutComponent, MainComponent],
  exports: [
    HeaderComponent,
    FooterComponent
  ],
  imports: [
    CommonModule
  ]
})
export class HomeModule { }
