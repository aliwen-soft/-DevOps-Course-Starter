import pymongo
from todo_app.data.todo_item import TodoItem, TODO_STATUS
from todo_app.data.db_client import Client
from bson.objectid import ObjectId
import datetime


def get_items_collection(config):
    client = Client.instance(config)
    db = client[config.DB_NAME]
    return db["items"]


def todo_from_doc(doc):
    return TodoItem(title=doc.get("title"), last_modified=doc.get(
        "last_modified"), status=doc.get("status"), id=doc.get(str("_id")))


def get_items(config):
    """
    Fetches all saved items from the database.

    Returns:
        list: The list of saved items.
    """

    items = get_items_collection(config=config)

    todos = [todo_from_doc(doc) for doc in items.find()]

    return todos


def get_item(config, id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """

    items = get_items_collection(config=config)
    doc = items.find_one(ObjectId(id))

    return todo_from_doc(doc)


def change_item_status(config, id, new_status):
    """
    Changes the item with specified id to specified status

    Args:
        id: The ID of the item.
        new_status: the status to be changed too

    """

    item = get_item(config=config, id=id)
    item.status = new_status
    item.last_modified = datetime.datetime.utcnow()

    items = get_items_collection(config=config)

    items.update_one(
        {"_id": ObjectId(item.id)},
        {"$set": item.__dict__}
    )

    return item


def add_item(config, title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    items = get_items_collection(config=config)

    new_item = {
        "status": TODO_STATUS,
        "title": title,
        "last_modified": datetime.datetime.utcnow()
    }

    items.insert_one(new_item)


def remove_item(config, id):
    """
    removes an item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: id of the item to remove.
    """

    items = get_items_collection(config=config)
    items.delete_one({'_id': ObjectId(id)})
