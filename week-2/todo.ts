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
  priority: ItemPriority,
  private: boolean
}


type TodoList = Array<TodoItem>

interface TodoListFilter {
  filterByStatus(list: TodoList, status: ItemState): TodoList,
  filterByPriority(list: TodoList, priority: ItemPriority): TodoList,
  filterByTitle(list: TodoList, title: string): TodoList
}



interface User {
  list: TodoList,
  friends: Array<User>,
  publicItems(): TodoList

}

interface ItemManipulator {
  createItem(
    itemTitle: string,
    status: ItemState,
    priority: ItemPriority,
    private: boolean,
    ): TodoItem,
    deletItem(item: TodoItem): TodoItem,
    updateStatus(item: TodoItem, status: ItemState): TodoItem,
    updatePriority(item: TodoItem, priority: ItemPriority): TodoItem,
    updatePrivacy(item: TodoItem, privacy: boolean): TodoItem
}

interface TodoApp {
  user: User,
  filter: TodoListFilter,
  itemManipulator: ItemManipulator,
  createList(): TodoList,
  viewUserList(user: User): TodoList,
  viewFriendsList(friends: Array<User>): TodoList
  findItemWithSameTitle(users: Array<User>, item: TodoItem): TodoItem
}
// The UI could get the number of TodoItem's currently shown on the screen by showing the size of TodoList