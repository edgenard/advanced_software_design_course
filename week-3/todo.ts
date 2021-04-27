enum ItemState {
  DONE = 'Done',
  NOT_DONE = 'Not Done',
  IN_PROGRESS = 'In Progress',
  UNDER_REVIEW = 'Under Review',
  BLOCKED = 'Blocked'
}

enum ItemPriority {
  HIGH = 1,
  MEDIUM = 2,
  LOW = 3
}

interface TodoItem {
  title: string,
  state: ItemState
  priority: ItemPriority
}

interface TodoList {
  items: Array<TodoItem>,
}

interface TodoListFilter {
  filterByStatus(list: TodoList, status: ItemState): TodoList,
  filterByPriority(list: TodoList, priority: ItemPriority): TodoList
}

interface TodoApp {
  list: TodoList,
  filter: TodoListFilter,
  createItem(itemTitle: string): TodoList,
  deleteItem(item: TodoItem): TodoList,
  viewList(): TodoList,
  updateStatus(item: TodoItem, status: ItemState): TodoList,
}
