https://gist.github.com/edgenard/b2f8b225cbcb20526a21389110c21a32

```Typescript
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
```

<------------ Feedback -------------->
Consider using a an enum for TodoStatus instead of booleans. As a common rule, where there are N of something, there may soon be N+1. The predictable addition of more statuses will force the solution to move away from boolean statuses, and so there will be more work in the next revision than if it had used an enum.

Good job having a type for TodoList.

Exposing the inwards of the `TodoList` will make changing the current representation that uses an `Array<TodoItem>` to some other possible representation really hard, because other units of code will be accessing the property items directly. Consider making `items` private and only exposing the minimum necessary function to provide the necessary functionality. In this case, add and remove a todo item.

Note that by having the `TodoApp` creating the `TodoItem` instead of just receiving it, it creates a dependency from `TodoApp` towards the data that's necessary to create a `TodoItem`. Meaning that whenever the necessary information to create a `TodoItem` changes, `createItem()` will have to change as well. Better to have `TodoApp` receive a `TodoItem` directly (E.g. `addTodo(TodoItem)`).

<------------------------------------>

```Typescript
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
  updatePriority(item: TodoItem, priority: ItemPriority): TodoList
}
```

<------------ Feedback -------------->
Good job using an enum for priorities.

In Week 5, there's an optional reading on defunctionalization/refunctionalization.
Having a `TodoListFilter` limited to `status` and `priority` is an example of defunctionalization.
The defunctionalized form is more inspectable while the lambda form (refunctionalized) is more open
It would be better to use a high order function since there is no real gain from using the defunctionalized for this application.
So instead of a `TodoListFilter` interface there would be a method on TodoList such as `filterTodoList(filter: (todo: TodoItem) => boolean): TodoItem`.
<------------------------------------>

```Typescript
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

// TodoList should have been defined like this the whole time. I'm still learning Typescript.
type TodoList = Array<TodoItem>

interface TodoListFilter {
  filterByStatus(list: TodoList, status: ItemState): TodoList,
  filterByPriority(list: TodoList, priority: ItemPriority): TodoList,

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
  viewList(user: User): TodoList,
  viewFriendsList(user: User): TodoList

}
```

<------------ Feedback -------------->
Good job building some privacy into the API by having user as a necessary parameter to get a TodoList.

Same feedback about booleans given in round 0 applies to privacy field in this round.
<------------------------------------>

```Typescript

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

```

<------------ Feedback -------------->
There might be a privacy leak in this design.

This design exercise has many challenges, but it revolves around one: building a representation and API that “bakes in” privacy. The challenges in the final revision are both designed to make it easy to forget about privacy and accidentally create a privacy leak.

The privacy leak for the first option comes from not taking into account that some items are private and should not be counted. This can be easily dodged if the feature is built on top of an existing API that bakes in privacy. Whether the answer above dodges the privacy violation will depend on how `findItemWithSameTitle` is implemented. If it is implemented using methods that already filter out private items, as it seems to be the case for `viewFriendList` and `publicItems` then everything should be ok. If it accesses an `Array<TodoItem` directly, unless there's code specific for filtering out private items, there will be a privacy violation.
<------------------------------------>
