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
              <button type="button" for="Insert" (click)="removeItem(ws.id)">Remove</button>
              <button type="button" name="Insert" (click)="insertItemAfterComponent(ws.id)">Insert new aria</button>
            </div>
            <textarea class="codeAria" (input)="onItemEdit($event.target, ws.id)"
                      rows="{{ws.itemText.split('\n').length}}">{{ws.itemText}}
            </textarea>
            <div class='result'>
              <div *ngFor="let out of ws.out">
                <div class="out.text" *ngIf="out.type === 'text'">
                  {{out.data}}
                </div>
              </div>
            </div>
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
      const newWorkSpace = new Workspace();
      newWorkSpace.loadData(JSON.parse(workspace));
      newWorkSpace.sortItems();
      this.workspace = newWorkSpace
    })
  }

  insertItemAfterComponent(componentID) {
    console.log('insert click');
    this.workspaceSerivce.addWorkspace(this.workspace.id, componentID)
      .subscribe(items => {
        const jsonArray = JSON.parse(items);
        this.workspace.insertNewItem(jsonArray.newItem);
        this.workspace.updateOrders(jsonArray.ID_OrderMap)
      })
  }

  removeItem(componentID): void {
    if (this.workspace.getUserEditItems() < 2) {
      alert('Please go away I wont thinking')
      return
    }
    this.workspaceSerivce.removeWorkspace(this.workspace.id, componentID)
      .subscribe(items => {
        const jsonArray = JSON.parse(items);
        this.workspace.removeByID(jsonArray.removedItemID);
        this.workspace.updateOrders(jsonArray.ID_OrderMap)
      })
  }

  onItemEdit(item, componentID): void {
    let lineCount = item.value.split('\n').length;
    const isChange = (lineCount !== item.rows)
    if (lineCount < 2) {
      lineCount = 2
    }
    item.rows = lineCount;
    if (isChange) {
      this.workspaceSerivce.pushCodeChange(this.workspace.id, componentID, item.value).subscribe(items => {
          console.log(items);
          this.workspace.updateResults(JSON.parse(items).out);
        }
      )
    }
  }

}
