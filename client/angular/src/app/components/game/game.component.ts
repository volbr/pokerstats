import { Component, OnInit } from '@angular/core';
import { DataService } from "../../services/data.service";
import { Game, Player } from "../../models";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent implements OnInit {

  player: Player;
  game: Game;
  currentGame: boolean = true;

  constructor(private activatedRoute: ActivatedRoute, private dataService: DataService) { }

  ngOnInit() {
    let finishedGame = this.activatedRoute.snapshot.params['id'];
    if (finishedGame) {
      this.currentGame = false;
      this.updateGame(finishedGame)
    } else {
      this.dataService.getPlayer().subscribe(player => {
      this.player = player;
      if (player.game) {
        this.updateGame(this.player.game)
      }
    })
    }
  }

  updateGame(game) {
    this.dataService.getGame(game).subscribe(game => {
      // TODO: error handling
      this.game = game;
    })
  }

}
