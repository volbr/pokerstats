import { Component, OnInit } from '@angular/core';

import { DataService } from "../../services/data.service";
import {Game, Player} from "../../models";
import { Router } from "@angular/router";

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  player: Player;
  game: number;
  games: Game[];

  constructor(private dataService: DataService, private router: Router) { }

  ngOnInit() {
    this.dataService.getPlayer().subscribe(player => {
      this.player = player;
      this.game = player.game
    });
    this.dataService.getGames().subscribe(games => {
      // TODO: error handling
      this.games = games;
      this.setSelectedPlayer()
    })
  }

  gameCreated($event) {
    this.player = $event;
    this.game = $event.game;

    // Update cache && redirect
    this.dataService.setPlayerCurrentGame($event.game);
    this.router.navigate(['/home/game'])
  }

  setSelectedPlayer() {
    for(let i = 0; i < this.games.length; i++) {
      this.games[i].selected = this.games[i].results[0].player.id;
    }
  }

  changeSelected(gameId, playerId) {
    for(let i = 0; i < this.games.length; i++) {
      if (gameId == this.games[i].id) {
        this.games[i].selected = playerId;
      }
    }
  }

}
