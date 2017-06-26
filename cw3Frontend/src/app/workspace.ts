/**
 * Created by yurabraiko on 26.06.17.
 */
export class WorkspaceItem {
  itemText: string;
  isEditable: boolean;
  id: string;
  constructor() {
    this.itemText = '';
    this.isEditable = true;
    this.id = '-1';
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
  }
}

