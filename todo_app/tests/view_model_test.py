import datetime
from _pytest.fixtures import fixture
from todo_app.view_model import ViewModel
from todo_app.data.todo_item import TodoItem, TODO_STATUS, DOING_STATUS, DONE_STATUS
import pytest
import datetime
from freezegun import freeze_time

test_now = datetime.datetime(2021, 11, 11, 10, 00, 55)
test_today = datetime.datetime(2021, 11, 11, 9, 00, 55)
test_yesterday = datetime.datetime(2021, 11, 10, 10, 00, 55)

@pytest.fixture
def item_view_model():
    items=[
        TodoItem(0,"item to do", test_today ,TODO_STATUS),
        TodoItem(1,"item to do #2",test_today,TODO_STATUS),
        TodoItem(2,"item doing",test_today ,DOING_STATUS),
        TodoItem(3,"item doing #2",test_today,DOING_STATUS),
        TodoItem(4,"item done",test_today,DONE_STATUS),
        TodoItem(5,"item done #2",test_today,DONE_STATUS),
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

def test_should_show_all_done_items_when_less_then_five(item_view_model):
    assert item_view_model.should_show_all_done_items

def test_should_not_show_all_done_items_when_five_or_more():
    items=[
        TodoItem(0,"item done",test_today, DONE_STATUS),
        TodoItem(1,"item done",test_today, DONE_STATUS),
        TodoItem(2,"item done",test_today, DONE_STATUS),
        TodoItem(3,"item done",test_today, DONE_STATUS),
        TodoItem(4,"item done",test_today, DONE_STATUS),
    ]
    view_model = ViewModel(items)

    assert not view_model.should_show_all_done_items

@freeze_time(test_now)
def test_show_today_items():
    items=[
        TodoItem(0,"item done",test_today, DONE_STATUS),
        TodoItem(1,"item done",test_today, DONE_STATUS),
        TodoItem(2,"item done",test_today, DONE_STATUS),
        TodoItem(3,"item done",test_yesterday, DONE_STATUS),
        TodoItem(4,"item done",test_yesterday, DONE_STATUS),
    ]

    view_model = ViewModel(items)
    items = view_model.recent_done_items

    assert len(items) == 3
    assert any(item.id == 0 for item in items)
    assert any(item.id == 1 for item in items)
    assert any(item.id == 2 for item in items)
    assert not any(item.id == 3 for item in items)
    assert not any(item.id == 4 for item in items)

@freeze_time(test_now)
def test_show_older_items():
    items=[
        TodoItem(0,"item done",test_today, DONE_STATUS),
        TodoItem(1,"item done",test_today, DONE_STATUS),
        TodoItem(2,"item done",test_today, DONE_STATUS),
        TodoItem(3,"item done",test_yesterday, DONE_STATUS),
        TodoItem(4,"item done",test_yesterday, DONE_STATUS),
    ]

    view_model = ViewModel(items)
    items = view_model.older_done_items

    assert len(items) == 2
    assert not any(item.id == 0 for item in items)
    assert not any(item.id == 1 for item in items)
    assert not any(item.id == 2 for item in items)
    assert any(item.id == 3 for item in items)
    assert any(item.id == 4 for item in items)



