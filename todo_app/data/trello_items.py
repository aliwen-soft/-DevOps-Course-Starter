import requests
from todo_app.flask_config import Config
from todo_app.data.todo_item import TodoItem, TODO_STATUS
from todo_app.api_exception import ApiException
import datetime


TRELLO_BASE_URL="https://api.trello.com"

def get_auth_payload(config):
    return {"key": config.TRELLO_API_KEY, "token": config.TRELLO_API_TOKEN}
       

def trello_date_time_to_date_time(date_time_str):
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return(date_time_obj)

def get_items(config):
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    auth_payload = get_auth_payload(config)
  
    url = TRELLO_BASE_URL+ "/1/boards/" + config.TRELLO_BOARD_ID + "/cards"

    params = {**auth_payload , "fields":"id,name,dateLastActivity,idList" } 

    r=requests.get(url=url, params=params)

    if r.status_code == 200:

        response = r.json()

        todo_items = map(
            lambda response_item: TodoItem(
                response_item.get("id"),
                response_item.get("name"),
                trello_date_time_to_date_time(response_item.get("dateLastActivity")),
                get_status_from_response_item(config, response_item)
                ),
            response
            )
    
        return todo_items
    
    raise ApiException(r.status_code,"There was an issue while trying to get items")

def get_item(config, id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items(config)

    item = next((item for item in items if item['id'] == int(id)), None)

    if item:
        return item

    raise ApiException(404 ,"That item does not exist")
    
def change_item_status(config, id, new_status):
    """
    Changes the item with specified id to specified status 

    Args:
        id: The ID of the item.
        new_status: the status to be changed too

    """

    auth_payload = get_auth_payload(config)

    list_id = get_list_id_with_list_name(config, new_status)

    update_card_url = TRELLO_BASE_URL+ "/1/cards/" + id
    update_card_params = {**auth_payload , "idList":list_id } 

    r=requests.put(url=update_card_url, params=update_card_params)
    if r.status_code != 200:
        raise ApiException(r.status_code,"There was an while trying to change item status")
    
def add_item(config, title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    auth_payload = get_auth_payload(config)

    todo_list_Id = get_list_id_with_list_name(config, TODO_STATUS)

    make_card_url = TRELLO_BASE_URL+ "/1/cards/"
    make_cards_params = {**auth_payload , "name":title, "idList": todo_list_Id } 

    r=requests.post(url=make_card_url, params=make_cards_params)
    
    if r.status_code == 200:

        respose_item = r.json()

        return TodoItem(respose_item.get("id"), respose_item.get("name"), respose_item.get("dateLastActivity"))

    raise ApiException(r.status_code,"There was an issue while trying to create an item")

def remove_item(config, id):
    """
    removes an item in the session. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: id of the item to remove.
    """

    auth_payload = get_auth_payload(config)

    delete_card_url = TRELLO_BASE_URL+ "/1/cards/" + id
    r = requests.delete(url=delete_card_url, params=auth_payload)
    if r.status_code != 200:
        raise ApiException(r.status_code,"There was an error while trying to remove card: "+id)

def get_status_from_response_item(config, item):

    auth_payload = get_auth_payload(config)

    id_list = item.get("idList")
    list_url = TRELLO_BASE_URL+ "/1/lists/" + id_list
    list_params = {**auth_payload , "fields":"name" } 

    r = requests.get(url=list_url, params=list_params)
    status = r.json().get("name")
    return status

def get_list_id_with_list_name(config, name):

    auth_payload = get_auth_payload(config)

    lists_url = TRELLO_BASE_URL+ "/1/board/"+config.TRELLO_BOARD_ID+"/lists/"
    lists_params = {**auth_payload , "fields":"id,name" } 
    r = requests.get(url=lists_url, params=lists_params)
    lists = r.json()
    list_with_name = next(list for list in lists if list.get("name")==name)
    return list_with_name.get("id")
  
    

