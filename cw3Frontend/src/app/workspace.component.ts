/**
 * Created by yurabraiko on 26.06.17.
 */
import {Component, ElementRef, Injectable, Input, OnInit, ViewChild} from '@angular/core';
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
      <ul class="documentItemList" #documentItemList>
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
                <div class="out.text" *ngIf="out.type === 'text'" id="{{out.order}}_{{ws.id}}">
                  {{decorateTextOut(out.data, out.order, ws.id)}}
                </div>
                <div class="out.base64image" *ngIf="out.type === 'base64'">
                  <img src='{{out.data}}'/>
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
  lastUpdateID = 0;

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

  decorateTextOut(raw: string, order: number, elementID: string): string {
    let result = raw;
    const regex = /\*\*([0-9]+)/g;
    let m = regex.exec(result);
    while (m !== null) {
      if (m.index === regex.lastIndex) {
        regex.lastIndex++;
      }
      result = result.replace(m[0], `<sup>${m[1]}</sup>`)
      m = regex.exec(result);
    }
    result = result.replace(/\*/g, '⋅');
    window.document.getElementById(order + '_' + elementID).innerHTML = `<p>${result}</p>`;
    return '';
  }

  onItemEdit(item, componentID): void {
    let lineCount = item.value.split('\n').length;
    if (lineCount < 2) {
      lineCount = 2
    }
    item.rows = lineCount;
    const update = (args) => {
      if (args[0] !== args[1].lastUpdateID) {
        return;
      }
      let message: string = item.value;
      const regex = /\\\s*\n/g;
      message = message.replace(regex, '');
      this.workspaceSerivce.pushCodeChange(this.workspace.id, componentID, message).subscribe(items => {
          console.log(items);
          this.workspace.updateResults(JSON.parse(items).out);
        }
      )
    };
    this.lastUpdateID++;
    setTimeout(update, 1000, [this.lastUpdateID, this]);

  };

}
