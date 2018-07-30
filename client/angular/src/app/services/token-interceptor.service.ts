import { Injectable } from '@angular/core';
import {
  HttpErrorResponse,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse
} from "@angular/common/http";
import { AuthService } from "./auth.service";
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor {

  constructor(private authService: AuthService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    let token = localStorage.getItem('token') || '';
    let tokenizedRequest = req.clone({
      setHeaders: {
        Authorization: `JWT ${token}`
      }
    });
    return next.handle(tokenizedRequest)
      .pipe(tap(
          // Succeeds when there is a response; ignore other events
          event => {
            if (event instanceof HttpResponse) {
              // do stuff with response if you want
              }
            },
          // Operation failed; error is an HttpErrorResponse
          error => {
            if (error instanceof HttpErrorResponse) {
              if (error.status === 401) {
                this.authService.logout()
              }
            }}
          ))
  }
}
