from todo_app.data.todo_item import DOING_STATUS, DONE_STATUS, TODO_STATUS

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return list(filter(lambda item: item.status == TODO_STATUS, self._items))

    @property
    def doing_items(self):
        return list(filter(lambda item: item.status == DOING_STATUS, self._items))

    @property
    def done_items(self):
        return list(filter(lambda item: item.status == DONE_STATUS, self._items))

