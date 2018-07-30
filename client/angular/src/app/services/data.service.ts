import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { of } from 'rxjs';

import {Game, Player, Rebuy, Round} from "../models";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class DataService {
  player: Player;

  constructor(private http: HttpClient) { }

  public finishGame(results: any) {
    return this.http.post('/api/game_finish/', results, httpOptions)
  }

  public createGame(game: Game) {
    return this.http.post('/api/game_create/', game, httpOptions)
  }

  public updateRound(round: Round) {
    return this.http.patch(`/api/round_update/${round.id}/`, round, httpOptions)
  }

  public createRebuy(rebuy: Rebuy) {
    return this.http.post('/api/rebuy_create/', rebuy, httpOptions)
  }

  public getGame(pk) {
    return this.http.get<Game>(`/api/game/${pk}/`)
  }

  public getGames() {
    return this.http.get<Game[]>(`/api/games/`)
  }

  public setPlayerCurrentGame(game) {
    if (this.player) {
      this.player.game = game
    }
  }
  // Tried to cache Player object, probably not a good approach to do it
  public getPlayer(refresh=false) {
    if (!refresh && this.player) {
      return of(this.player)
    } else {
      let playerRequest = this.http.get<Player>('/api/player/');
      playerRequest.subscribe(player => { this.player = player });
      return playerRequest;
    }
  }
}
