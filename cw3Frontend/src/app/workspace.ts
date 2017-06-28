import {until} from "selenium-webdriver";
import titleMatches = until.titleMatches;
/**
 * Created by yurabraiko on 26.06.17.
 */
export class WorkspaceItem {
  itemText: string;
  isEditable: boolean;
  id: string;
  order: number;
  out: any[];

  constructor() {
    this.itemText = '';
    this.isEditable = true;
    this.id = '-1';
    this.order = 0
    this.out = []
  }

  updateOut(out) {
    this.out = out
  }

  loadData(item: any) {
    if ('itemText' in item) {
      this.itemText = item.itemText
    }
    if ('isEditable' in item) {
      this.isEditable = item.isEditable
    }
    if ('id' in item) {
      this.id = item.id
    }
    if ('order' in item) {
      this.order = item.order
    }
    if ('out' in item) {
      this.out = item.out
    }
  }
}

export class Workspace {
  id: string;
  title: string;
  inputList: WorkspaceItem[];

  constructor() {
    this.id = '-1';
    this.title = 'Blank';
    this.inputList = []
  };

  public insertNewItem(data) {
    const item = new WorkspaceItem();
    item.loadData(data);
    this.inputList.push(item);
  };

  public sortItems() {
    this.inputList.sort((a, b) => b.order - a.order);
  };

  public removeByID(itemID) {
    const clearedItems = [];
    for (let i = 0; i < this.inputList.length; i++) {
      if (this.inputList[i].id.toString() === itemID) {
        continue
      }
      clearedItems.push(this.inputList[i])
    }
    this.inputList = clearedItems
  };

  public updateOrders(update) {
    for (const u of update) {
      for (let i = 0; i < this.inputList.length; i++) {
        if (this.inputList[i].id === u.id) {
          this.inputList[i].order = u.order
        }
      }
    }
    this.sortItems()
  };

  public getUserEditItems() {
    let result = 0;
    for (const i of this.inputList) {
      if (i.isEditable) {
        result += 1;
      }
    }
    return result;
  };

  applyToItem(id, action) {
    for (const i of this.inputList) {
      if (i.id === id) {
        action(i);
        return
      }
    }
  };

  public updateResults(responce) {
    for (const res of responce) {
      this.applyToItem(res.put_id, i => i.updateOut(res.items))
    }
  };

  public loadData(item: any) {
    if ('id' in item) {
      this.id = item.id
    }
    if ('title' in item) {
      this.title = item.title
    }
    if ('inputList' in item) {
      this.inputList = [];
      for (let i = 0; i < item.inputList.length; i++) {
        const newItem = new WorkspaceItem();
        newItem.loadData(item.inputList[i]);
        this.inputList.push(newItem)
      }
    }
  };
}


