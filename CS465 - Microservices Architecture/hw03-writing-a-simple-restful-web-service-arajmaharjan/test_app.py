import pytest
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_activities_json_with_proper_mimetype(client):
    response = client.get('/api/activities')
    assert response.status_code == 200
    assert response.content_type == 'application/json' 

def test_new_activity_without_all_elements_errors(client):
    activity = {"user_id": "id", "username": "nick"}
    response = client.post('/api/activities', json=activity)
    assert response.status_code == 400