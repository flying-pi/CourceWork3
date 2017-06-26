/**
 * Created by yurabraiko on 26.06.17.
 */
import {Component, Injectable, OnInit} from '@angular/core';
import {WorkspaceService} from './workspace.service';

@Component({
  selector: 'app-root',
  styleUrls: ['./workspace.component.css'],
  providers: [WorkspaceService],
  template: `
    <h1>{{title}}</h1>
    <div>
      <div>
        <label for="Name">Workspace name: </label>
        <input [(ngModel)]="workspaceName" name="Name">
      </div>
      <!--<textarea class="codeAria" [(ngModel)]="workspaceName" ></textarea>-->
      <textarea class="codeAria"></textarea>
    </div>
  `
})

@Injectable()
export class WorkspaceComponent implements OnInit {
  title = 'Workspace';
  workspaceName = 'Tour of Heroes';
  codePuts = [];

  constructor(private workspaceSerivce: WorkspaceService) {
  }

  ngOnInit(): void {
    console.log('befor calling loading');
    const result = this.workspaceSerivce.loadWorkspace('-1');
    result.forEach(value => console.log(value.toString()));
    console.log('after calling loading');
    // $http({
    //   method: 'GET',
    //   url: '/getWorkspace',
    //   params: {id: -1}
    // }).then(function successCallback(response) {
    //   $window.alert('successCallback');
    // }, function errorCallback(response) {
    //   $window.alert('errorCallback');
    // });
  }
}
