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
        # Limpia la base de datos después de cada prueba
        with app.app_context():
            db.drop_all()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/add', data={'title': 'Tarea'})
    assert response.status_code == 302  # Redirect to index
    with app.app_context():
        task = Task.query.first()
        assert task.title == 'Tarea'

def test_view_task_list(client):
    # Verifica que las tareas sean visibles en la página principal
    with app.app_context():
        db.session.add(Task(title='Tarea 1'))
        db.session.commit()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Tarea 1' in response.data

def test_complete_task(client):
    # Verifica que se pueda completar una tarea
    with app.app_context():
        task = Task(title='Tarea Completar')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    response = client.get(f'/complete/{task_id}')
    assert response.status_code == 302
    with app.app_context():
        task = Task.query.get(task_id)
        assert task.completed is True

def test_delete_task(client):
    # Verifica que se pueda eliminar una tarea
    with app.app_context():
        task = Task(title='Tarea Eliminar')
        db.session.add(task)
        db.session.commit()
        task_id = task.id
    response = client.get(f'/delete/{task_id}')
    assert response.status_code == 302
    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None

def test_add_invalid_task(client):
    # Verifica que no se puedan agregar tareas con datos inválidos
    response = client.post('/add', data={'title': ''})  # Título vacío
    assert response.status_code == 400  # Código de error esperado
    with app.app_context():
        task = Task.query.first()
        assert task is None

# Permite ejecutar las pruebas desde el script si es necesario
if __name__ == '__main__':
    pytest.main(['-v'])
