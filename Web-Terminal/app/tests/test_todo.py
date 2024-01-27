from flask                import url_for
from app.tests.conftest   import client, init_database, log_in_default_user, todo
from ..bundle.todo.models import Todo


def test_todo_model():
    todo = Todo(title='Test', description='Description')
    assert todo.title == 'Test'
    assert todo.description == 'Description'
    assert not todo.status


def test_todo_add(client, init_database, log_in_default_user):
    data = {
        'title': 'New task to be done',
        'description': 'This description'
    }
    response = client.post(url_for('todo.todo_list'), data=data, follow_redirects=True)
    assert response.status_code == 200


def test_todo_update(client, init_database, log_in_default_user, todo):
    response = client.get(url_for('todo.todo_status', id=1), follow_redirects=True)
    updated_todo = Todo.query.filter_by(id=todo[0].id).first()
    assert response.status_code == 200
    assert updated_todo.status


def test_todo_delete(client, init_database, log_in_default_user, todo):
    to_be_deleted = todo[0].id
    response = client.get(url_for('todo.todo_remove', id=to_be_deleted), follow_redirects=True)
    deleted_todo = Todo.query.get(to_be_deleted)
    assert deleted_todo is None
