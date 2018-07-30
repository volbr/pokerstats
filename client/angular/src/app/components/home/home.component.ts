import {Component, OnInit } from '@angular/core';

import {DataService} from "../../services/data.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  currentTeam: string;

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataService.getPlayer().subscribe(player => {
      this.currentTeam = player.team.name
    })
  }

}
