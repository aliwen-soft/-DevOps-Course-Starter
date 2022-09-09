TODO_STATUS = "To Do"
DOING_STATUS = "Doing"
DONE_STATUS = "Done"


class TodoItem:
    def __init__(self, id, title, last_modified, status=TODO_STATUS):
        self.id = id
        self.status = status
        self.title = title
        self.last_modified = last_modified

    def get_ordering_index(self):
        return 1 if self.status == DONE_STATUS else 0.5 if self.status == DOING_STATUS else 0
