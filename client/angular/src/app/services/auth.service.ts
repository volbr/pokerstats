import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private httpOptions: any;
  public errors: any = [];

  constructor(private http: HttpClient, private router: Router) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
  }

  public login(user) {
    this.http.post('/api/token-auth/', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
        localStorage.setItem('token', data['token']);
        this.router.navigate(['/home/games']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  public logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

}
