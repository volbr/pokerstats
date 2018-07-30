import {Component, OnInit, Input, ViewChild, Output, EventEmitter} from '@angular/core';
import {Game, Rebuy} from "../../../models";
import { DataService } from "../../../services/data.service";

@Component({
  selector: 'app-rebuy-form',
  templateUrl: './rebuy-form.component.html',
  styleUrls: ['./rebuy-form.component.css']
})
export class RebuyFormComponent implements OnInit {

  @Input() game: Game;
  @Output() newRebuyEvent = new EventEmitter<null>();
  @ViewChild('form') form: any;
  @ViewChild('closeModal') closeModal: any;
  rebuy: Rebuy = {player: null, amount: null, round: null};

  constructor(private dataService: DataService) { }

  ngOnInit() {
  }

  onSubmit() {
    this.rebuy.round = this.game.round;
    this.dataService.createRebuy(this.rebuy).subscribe(rebuy => {
      // TODO: error handling
      this.form.reset();
      this.closeModal.nativeElement.click();
      this.newRebuyEvent.emit();
    });
  }

}
