from _pytest.fixtures import fixture
from todo_app.view_model import ViewModel
from todo_app.data.todo_item import TodoItem, TODO_STATUS, DOING_STATUS, DONE_STATUS
import pytest

@pytest.fixture
def item_view_model():
    items=[
        TodoItem(0,"item to do",TODO_STATUS),
        TodoItem(1,"item to do #2",TODO_STATUS),
        TodoItem(2,"item doing",DOING_STATUS),
        TodoItem(3,"item doing #2",DOING_STATUS),
        TodoItem(4,"item done",DONE_STATUS),
        TodoItem(5,"item done #2",DONE_STATUS),
    ]
    return ViewModel(items)


def test_get_items(item_view_model):
    assert len(item_view_model.items) == 6

def test_get_todo(item_view_model):
    items = item_view_model.todo_items

    assert len(items) == 2
    assert any(item.id == 0 for item in items)
    assert any(item.id == 1 for item in items)

def test_get_doing(item_view_model):
    items = item_view_model.doing_items

    assert len(items) == 2
    assert any(item.id == 2 for item in items)
    assert any(item.id == 3 for item in items)

def test_get_done(item_view_model):
    items = item_view_model.done_items

    assert len(items) == 2
    assert any(item.id == 4 for item in items)
    assert any(item.id == 5 for item in items)

