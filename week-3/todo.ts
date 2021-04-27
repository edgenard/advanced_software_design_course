

interface TodoItem {
  title: string,
  done: true | false
}

interface TodoList {
  items: Array<TodoItem>,
}


interface TodoApp {
  list: TodoList
  createItem(itemTitle: string): TodoList,
  deleteItem(item: TodoItem): TodoList,
  viewList(): TodoList
  markDone(item: TodoItem): TodoList
}