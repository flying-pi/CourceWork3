/**
 * Created by yurabraiko on 26.06.17.
 */
export class WorkspaceItem {
  itemText: string;
  isEditable: boolean;
  id: string;
  order: number;

  constructor() {
    this.itemText = '';
    this.isEditable = true;
    this.id = '-1';
    this.order = 0
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

  public insertNewItem(item) {
    this.inputList.push(item);
    this.inputList.sort((a, b) => b.order - a.order);
  };
}


