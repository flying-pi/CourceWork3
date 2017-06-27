/**
 * Created by yurabraiko on 26.06.17.
 */
import {Component, Injectable, Input, OnInit} from '@angular/core';
import {WorkspaceService} from './workspace.service';
import {Workspace, WorkspaceItem} from './workspace';

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
              <button type="button" for="Insert" (click)="removeItem(ws.id)">Remove</button>
              <button type="button" name="Insert" (click)="insertItemAfterComponent(ws.id)">Insert new aria</button>
            </div>
            <textarea class="codeAria" (input)="onItemEdit($event.target,ws.id)">{{ws.itemText}}</textarea>
          </div>
        </li>
      </ul>
      <button type="button" (click)="insertItemAfterComponent(-1)">Add new aria</button>
    </div>
  `
})

@Injectable()
export class WorkspaceComponent implements OnInit {
  @Input() workspace: Workspace = new Workspace();

  constructor(private workspaceSerivce: WorkspaceService) {
  }

  ngOnInit(): void {
    this.workspaceSerivce.loadWorkspace('-1').subscribe(workspace => {
      const newWorkSpace = Object.assign(new Workspace(), JSON.parse(workspace))
      newWorkSpace.sortItems();
      this.workspace = newWorkSpace
    })
  }

  insertItemAfterComponent(componentID) {
    console.log('insert click');
    this.workspaceSerivce.addWorkspace(this.workspace.id, componentID)
      .subscribe(items => {
        const jsonArray = JSON.parse(items);
        this.workspace.insertNewItem(Object.assign(new WorkspaceItem(), jsonArray.newItem));
        this.workspace.updateOrders(jsonArray.ID_OrderMap)
      })
  }

  removeItem(componentID): void {
    console.log('remove click');
  }

  onItemEdit(item, componentID): void {
    let lineCount = item.value.split('\n').length;
    if (lineCount < 2) {
      lineCount = 2
    }
    item.rows = lineCount;
    console.log('onItemEdit');
    console.log(item.textContent);
  }
}
