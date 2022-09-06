import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import mongomock
import os


@pytest.fixture
def client():
    filepath = find_dotenv(".env.test")
    load_dotenv(filepath, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_with_added_card(client):
    client.post('/add-todo', data=dict(title="I am a card"))
    response = client.get('/')

    html_response = response.data.decode()

    assert response.status_code == 200
    assert 'I am a card' in html_response
    assert 'Mark in progress' in html_response
