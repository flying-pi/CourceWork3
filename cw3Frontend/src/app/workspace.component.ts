/**
 * Created by yurabraiko on 26.06.17.
 */
import {Component, Injectable, Input, OnInit} from '@angular/core';
import {WorkspaceService} from './workspace.service';
import {Workspace} from './workspace';

@Component({
  selector: 'app-root',
  styleUrls: ['./workspace.component.css'],
  providers: [WorkspaceService],
  template: `
    <h1>{{workspace.title}}</h1>
    <div>
      <label>id :: {{workspace.id}}</label>
      <div>
        <label for="Name">Workspace name: </label>
        <input [(ngModel)]="workspace.title" name="Name">
      </div>
      <ul class="documentItemList">
        <li class="documentItem" *ngFor="let ws of workspace.inputList">
          <div>
            <div>
              <button type="button"  for="Insert" (click)="removeItem(ws.id)">Remove</button>
              <button type="button"  name="Insert" (click)="insertItem(ws.id)">Insert new aria</button>
            </div>
            <textarea class="codeAria">{{ws.itemText}}</textarea>
          </div>
        </li>
      </ul>
      <button type="button"  (click)="insertItem(-1)" >Add new aria</button>
    </div>
  `
})

@Injectable()
export class WorkspaceComponent implements OnInit {
  @Input() workspace: Workspace = new Workspace();

  constructor(private workspaceSerivce: WorkspaceService) {
  }

  ngOnInit(): void {
    this.workspaceSerivce.loadWorkspace('-1').subscribe(workspace => this.workspace = JSON.parse(workspace))
  }

  insertItem(componentID): void {

    console.log('insert click');
  }

  removeItem(componentID): void {
    console.log('remove click');
  }
}
