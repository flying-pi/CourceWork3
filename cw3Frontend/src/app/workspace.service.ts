/**
 * Created by yurabraiko on 26.06.17.
 */
import {Injectable} from '@angular/core';
import {Http, Response, Headers} from '@angular/http';

import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

@Injectable()
export class WorkspaceService {
  constructor(private http: Http) {
  }

  loadWorkspace(id: string) {
    console.log('calling loadWorkspace.....');
    const headers = new Headers();
    // headers.append('Access-Control-Allow-Headers', '*');
    headers.append('Accept', 'application/json');
    // return this.http.get('http://0.0.0.0:8000/api/getWorkspace')
    return this.http.get('http://127.0.0.1:8000/api/getWorkspace', {
      params: {id: id},
      headers: headers
    })
    // return this.http.get('http://127.0.0.1:8000/getWorkspace')
      .map(this.extractData)
      .catch(this.handleError);
  }

  private extractData(res: Response) {
    const body = res.json();
    console.log(res.toString());
    return body.data || {};
  }

  private handleError(error: Response | any) {
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Observable.throw(errMsg);
  }

}
