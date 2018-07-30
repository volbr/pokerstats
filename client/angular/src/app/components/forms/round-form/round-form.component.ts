import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {Game, Rebuy, Round} from "../../../models";
import {DataService} from "../../../services/data.service";

@Component({
  selector: 'app-round-form',
  templateUrl: './round-form.component.html',
  styleUrls: ['./round-form.component.css']
})
export class RoundFormComponent implements OnInit {

  @Input() game: Game;
  @Output() newRoundEvent = new EventEmitter<null>();
  @ViewChild('form') form: any;
  @ViewChild('closeModal') closeModal: any;
  combinations: string[] = [
    'High Card', 'Pair', 'Two Pairs', 'Three of a Kind', 'Straight',
    'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush'
  ];
  round: Round = {
    id: null,
    combination: null,
    winning: null,
    winner: null
  };

  constructor(private dataService: DataService) { }

  ngOnInit() {
  }

  onSubmit() {
    this.round.id = this.game.round;
    this.dataService.updateRound(this.round).subscribe(round => {
      this.newRoundEvent.emit();
      // TODO: close modal using styles
      this.closeModal.nativeElement.click();
      this.form.reset();
    });

  }
}
