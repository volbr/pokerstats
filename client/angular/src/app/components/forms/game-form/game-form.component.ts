import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {Game, Player} from "../../../models";
import {DataService} from "../../../services/data.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-game-form',
  templateUrl: './game-form.component.html',
  styleUrls: ['./game-form.component.css']
})
export class GameFormComponent implements OnInit {

  @Input() player: Player;
  @Output() newGameEvent = new EventEmitter<Player>();
  @ViewChild('closeModal') closeModal: any;
  game: Game;

  constructor(private dataService: DataService) {
  }

  ngOnInit() {
    this.game = {players: [], team: this.player.team.id, init_stake: null};
  }

  onSubmit() {
    // TODO: close modal using styles
    this.closeModal.nativeElement.click();
    this.game.players.push(this.player.id);
    this.game.creator = this.player.id;
    this.dataService.createGame(this.game).subscribe(game => {
      this.updatePlayer(game)
    });
  }

  updatePlayer(game) {
    this.player.game = game.id;
    this.newGameEvent.emit(this.player);
  }
}
