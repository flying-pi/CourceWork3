/**
 * Created by yurabraiko on 26.06.17.
 */
import {Injectable} from '@angular/core';
import {Headers, Http, Response} from '@angular/http';

import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import {Workspace} from './workspace';

@Injectable()
export class WorkspaceService {
  constructor(private http: Http) {
  }

  loadWorkspace(id: string) {
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    return this.http.get('http://127.0.0.1:8000/api/getWorkspace/', {
      params: {id: id},
      headers: headers
    }).map(res => {
      console.log('getting response ', res.toString());
      return res.json()
    })
      .catch(error => {
        this.handleError(error);
        return Observable.create(observer => {
          observer.next(new Workspace());
          observer.complete();
        });
      })
  }

  addWorkspace(workspaceID: string, workspaceItemID: string) {
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    const body = {
      workspaceID: workspaceID,
      workspaceItemID: workspaceItemID
    };

    return this.http.post(
      'http://127.0.0.1:8000/api/workspaceItem/',
      body,
      {headers: headers}
    ).map(res => {
      console.log('getting response ', res.toString());
      return res.json()
    })
      .catch(error => {
        this.handleError(error);
        return Observable.create(observer => {
          observer.next(new Workspace());
          observer.complete();
        });
      })
  }


  removeWorkspace(workspaceID: string, workspaceItemID: string) {
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    const body = {
      workspaceID: workspaceID,
      workspaceItemID: workspaceItemID
    };

    return this.http.delete(
      'http://127.0.0.1:8000/api/workspaceItem/',
      {
        params: body,
        headers: headers
      }
    ).map(res => {
      console.log('getting response ', res.toString());
      return res.json()
    })
      .catch(error => {
        this.handleError(error);
        return Observable.create(observer => {
          observer.next(new Workspace());
          observer.complete();
        });
      })
  }

  pushCodeChange(workspaceID: string, workspaceItemID: string, code: string) {
    const headers = new Headers();
    headers.append('Accept', 'application/json');
    headers.append('Content-Type', 'application/json');
    const body = {
      workspaceID: workspaceID,
      workspaceItemID: workspaceItemID,
      code: code
    };

    return this.http.post(
      'http://127.0.0.1:8000/api/code/',
      body,
      {headers: headers}
    ).map(res => {
      console.log('getting response ', res.toString());
      return res.json()
    })
      .catch(error => {
        this.handleError(error);
        return Observable.create(observer => {
          observer.next(new Workspace());
          observer.complete();
        });
      })
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
