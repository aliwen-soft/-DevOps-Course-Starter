from requests import get, put, post, delete
from todo_app.flask_config import Config
from todo_app.data.todo_item import TodoItem, TODO_STATUS, DOING_STATUS, DONE_STATUS

TRELLO_BASE_URL="https://api.trello.com"

config = Config()

auth_payload = {"key": config.TRELLO_API_KEY, "token": config.TRELLO_API_TOKEN}

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
  
    url = TRELLO_BASE_URL+ "/1/boards/" + config.TRELLO_BOARD_ID + "/cards"

    params = {**auth_payload , "fields":"id,name,idList" } 

    r=get(url=url, params=params)

    response = r.json()

    todo_items = map(
        lambda response_item: TodoItem(response_item.get("id"), response_item.get("name"),  get_status_from_response_item(response_item)),
        response
        )
   
    return todo_items

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)

def change_item_status(id, new_status):
    """
    Changes the item with specified id to specified status 

    Args:
        id: The ID of the item.
        new_status: the status to be changed too

    """
    list_id = get_list_id_with_list_name(new_status)

    update_card_url = TRELLO_BASE_URL+ "/1/cards/" + id
    update_card_params = {**auth_payload , "idList":list_id } 

    r=put(url=update_card_url, params=update_card_params)
    
def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    todo_list_Id = get_list_id_with_name(TODO_STATUS)

    make_card_url = TRELLO_BASE_URL+ "/1/cards/"
    make_cards_params = {**auth_payload , "name":title, "idList": todo_list_Id } 

    r=post(url=make_card_url, params=make_cards_params)
    print(r)

    respose_item= r.json()

    return TodoItem(respose_item.get("id"), respose_item.get("name"))

def remove_item(id):
    """
    removes an item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: id of the item to remove.
    """
    delete_card_url = TRELLO_BASE_URL+ "/1/cards/" + id
    r = delete(url=delete_card_url, params=auth_payload)

def get_status_from_response_item(item):
    id_list = item.get("idList")
    list_url = TRELLO_BASE_URL+ "/1/lists/" + id_list
    list_params = {**auth_payload , "fields":"name" } 
    r=get(url=list_url, params=list_params)
    status = r.json().get("name")
    return status

def get_list_id_with_list_name(name):
    lists_url = TRELLO_BASE_URL+ "/1/board/"+config.TRELLO_BOARD_ID+"/lists/"
    lists_params = {**auth_payload , "fields":"id,name" } 
    r=get(url=lists_url, params=lists_params)
    lists = r.json()
    list_with_name = next(list for list in lists if list.get("name")==name)
    return list_with_name.get("id")
  
    

