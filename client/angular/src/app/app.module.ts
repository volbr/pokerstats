import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AngularFontAwesomeModule } from 'angular-font-awesome';

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthGuard } from "./auth.guard";

import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { GameComponent } from './components/game/game.component';
import { GamesComponent } from './components/games/games.component';

import { AuthService } from './services/auth.service';
import { TokenInterceptorService} from "./services/token-interceptor.service";
import { DataService } from "./services/data.service";
import { RebuyFormComponent } from './components/forms/rebuy-form/rebuy-form.component';
import { GameFormComponent } from './components/forms/game-form/game-form.component';
import { FinishGameFormComponent } from './components/forms/finish-game-form/finish-game-form.component';
import { RoundFormComponent } from './components/forms/round-form/round-form.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    GameComponent,
    GamesComponent,
    RebuyFormComponent,
    GameFormComponent,
    FinishGameFormComponent,
    RoundFormComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    ReactiveFormsModule,
    AngularFontAwesomeModule
  ],
  providers: [AuthService, AuthGuard, DataService, {
    provide: HTTP_INTERCEPTORS,
    useClass: TokenInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
