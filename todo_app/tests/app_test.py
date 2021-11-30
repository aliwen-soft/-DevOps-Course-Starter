import os
import pytest
from dotenv import load_dotenv, find_dotenv
import requests
from todo_app import app

@pytest.fixture
def client():
    filepath = find_dotenv(".env.test")
    load_dotenv(filepath, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests,'get', mock_get)
    response = client.get('/')

    html_response = response.data.decode()
    
    assert response.status_code == 200
    assert 'I am a card' in html_response
    assert 'Mark in progress' in html_response
 
class StubResponse(): 
    def __init__(self, fake_response_data, status_code): 
        self.fake_response_data = fake_response_data 
        self.status_code = status_code
    def json(self): 
        return self.fake_response_data


def get_cards_stub(): 
    fake_response_data = [{ 
        'id': '123abc', 
        'name': 'I am a card', 
        'idList': 'lista',
        'dateLastActivity' : '2021-11-29T18:00:00.00Z'
    }] 
    return StubResponse(fake_response_data, 200)

def get_list_stub(): 
    fake_response_data = { 
        'id': 'lista', 
        'name': 'To Do',
    }
    return StubResponse(fake_response_data, 200)

def mock_get(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/cards': 
        return get_cards_stub()
    elif url.startswith('https://api.trello.com/1/lists/'): 
        return get_list_stub()
