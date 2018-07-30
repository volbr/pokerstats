import { NgModule } from '@angular/core';
import { RouterModule, Routes} from "@angular/router";

import { HomeComponent } from "./components/home/home.component";
import { GameComponent } from "./components/game/game.component";
import { GamesComponent } from "./components/games/games.component";
import { LoginComponent } from "./components/login/login.component";
import { AuthGuard } from "./auth.guard";

const routes: Routes = [
  { path: '', redirectTo: 'home/games', pathMatch: 'full' },
  {
    path: "home",
    component: HomeComponent,
    canActivate: [AuthGuard],
    children: [
      { path: "games", component: GamesComponent },
      { path: "game", component: GameComponent },
      { path: "game/:id", component: GameComponent },
    ]
  },
  // { path: "**", redirectTo: "/app/main/layout-a" },
  { path: 'login', component: LoginComponent },
];

@NgModule({
  exports: [RouterModule],
  imports: [
    RouterModule.forRoot(routes)
  ],
})
export class AppRoutingModule { }
