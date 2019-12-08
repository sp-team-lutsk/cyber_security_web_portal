import { Component, OnInit } from '@angular/core';
import {Chart} from 'chart.js';
import { faAngleDown, faAngleUp, faChartLine, faEdit } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-science',
  templateUrl: './science.component.html',
  styleUrls: ['./science.component.sass']
})
export class ScienceComponent implements OnInit {

  faAngleDown = faAngleDown;
  faAngleUp = faAngleUp;
  faChartLine = faChartLine;
  faEdit = faEdit;
  LineChart=[];

  constructor() { }

  ngOnInit() {
    //Графік відвідуваності
    this.LineChart = new Chart('lineChartVisit', {

     type: 'line',

    data: {
    labels: ["вересень", "жовтень", "листопад", "грудень", "січень", "лютий","березень","квітень","травень","червень"],
    datasets: [{
        label: 'Відвідуваність',
        data: [10,30 , 19, 30, 40, 42,45,68,78],
        pointRadius: 0,
        fill:false,
        lineTension:0,
        borderColor:"rgb(78, 188, 210)"

    }]
    },
    options: {
      responsive: false,
      legend: {
        display: false,
    },

    tooltips:{
        backgroundColor: "white",
        titleFontColor: "black",
        bodyFontColor: "black",
        footerFontColor: "black"

        },
    scales: {
        yAxes: [{
            gridLines: {
              color:"black"
            },
            ticks: {
                beginAtZero:true
            }
        }],
        xAxes: [{

          gridLines: {
            drawTicks:true,
            display:false
          }
        }]
    }
    }
    });

    //Графік успішності
    this.LineChart = new Chart('lineChartSuccess', {

     type: 'line',

    data: {
    labels: ["вересень", "жовтень", "листопад", "грудень", "січень", "лютий","березень","квітень","травень","червень"],
    datasets: [{
        label: 'Успішність',
        data: [10,30 , 19, 30, 40, 42,45,68,78],
        pointRadius: 0,
        fill:false,
        lineTension:0,
        borderColor:"rgb(78, 188, 210)"
    }]
    },
    options: {
      responsive: false,
      legend: {
        display: false,
    },

      tooltips:{
            backgroundColor: "white",
            titleFontColor: "black",
            bodyFontColor: "black",
            footerFontColor: "black"

        },
    scales: {
        yAxes: [{
            gridLines: {
              color:"black"
            },
            ticks: {
                beginAtZero:true
            }
        }],
        xAxes: [{

          gridLines: {
            drawTicks:true,
            display:false
          }
        }]
    }
    }
    });
  }

}
