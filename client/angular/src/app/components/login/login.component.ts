import { Component, OnInit } from '@angular/core';
import {AuthService} from '../../services/auth.service';

import { Router } from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  public user: any;

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
    if (localStorage.getItem('token')) {
      this.router.navigate(['/home/games'])
    }
    this.user = {
      username: '',
      password: ''
    };
  }

  login() {
    this.authService.login({'username': this.user.username, 'password': this.user.password});
  }

  logout() {
    this.authService.logout();
  }

}
