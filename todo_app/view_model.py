from datetime import datetime
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

    @property
    def should_show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self):
        return list(filter(lambda item: item.last_modified.day == datetime.now().day , self._items))

    @property
    def older_done_items(self):
        return list(filter(lambda item: item.last_modified.day < datetime.now().day , self._items))

