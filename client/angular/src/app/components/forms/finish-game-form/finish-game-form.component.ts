import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, FormArray, Validators, FormBuilder } from '@angular/forms'
import { Game } from "../../../models";
import { DataService } from "../../../services/data.service";
import { Router } from "@angular/router";

@Component({
  selector: 'app-finish-game-form',
  templateUrl: './finish-game-form.component.html',
  styleUrls: ['./finish-game-form.component.css']
})
export class FinishGameFormComponent implements OnInit {

  @Input() game: Game;
  @ViewChild('closeModal') closeModal: any;
  gameResultsForm:FormGroup;

  constructor(private fb:FormBuilder, private dataService: DataService, private router: Router) { }

  ngOnInit() {
    this.createForm();
    this.addResults()
  }

  createForm() {
    this.gameResultsForm = this.fb.group({
      results: this.fb.array([])
	  });
  }

  addResults() {
    for (let i = 0; i < this.game.players.length; i++) {
      let player = this.game.players[i];
	    this.resultsFormArray.push(this.initResult(player));
    }
  }

  initResult(player) {
    return this.fb.group({
      game: this.game.id,
      player: player.id,
      playerName: player.name,
      stake: new FormControl('', Validators.required)
    })
  }

  get resultsFormArray(): FormArray {
	  return this.gameResultsForm.get('results') as FormArray;
  }

  onSubmit() {
    this.dataService.finishGame(this.resultsFormArray.value).subscribe(results => {
      // TODO: error handling
      this.dataService.setPlayerCurrentGame(null);
      this.closeModal.nativeElement.click();
      this.router.navigate(['/home/games'])
    });
  }
}
