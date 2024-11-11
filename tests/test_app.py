import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/add', data={'title': 'Test Task'})
    assert response.status_code == 302  # Redirect to index
    task = Task.query.first()
    assert task.title == 'Test Task'
