import unittest

from flask import url_for

from app import db
from app.bundle.accounts.models import User
from app.bundle.todo.models import Todo
from tests.base import BaseTestCase


class TodoTests(BaseTestCase):
    def test_todo_create(self):
        """
        Test creation of a todo item
        """
        data = {
            'title': 'Write flask tests',
            'description': 'New description',
        }
        with self.client:
            response = self.client.post(url_for('todo.todo_list'), data=data, follow_redirects=True)
            assert response.status_code == 200
            todo = Todo.query.get(1)
            assert todo.title == data['title']

    def test_get_all_todo(self):
        """
        Test retrieving all todo items
        """
        todo_1 = Todo(title="todo1", description="description1", status=False)
        todo_2 = Todo(title="todo2", description="description2", status=False)
        db.session.add_all([todo_1, todo_2])
        all_todo = Todo.query.count()
        assert all_todo == 2

    def test_update_todo(self):
        """
        Test updating a todo item to
        """
        user = User(username='test_user', password='password')
        db.session.add(user)
        todo_1 = Todo(title="todo1", description="description1", status=True)
        db.session.add(todo_1)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(username='test_user', password='password', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.get(url_for('todo.todo_status', id=1), follow_redirects=True)
            todo = Todo.query.get(1)
            assert todo.status is False

    def test_delete_todo(self):
        """
        Test deleting a todo item
        """
        user = User(username='test_user', password='password')
        db.session.add(user)
        todo = Todo(title="todo", description="description", status=False)
        db.session.add(todo)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(username='test_user', password='password', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            response = self.client.post(url_for('todo.todo_remove', id=1), follow_redirects=True)
            assert response.status_code == 200
            deleted_todo = Todo.query.get(1)
            assert deleted_todo is None

    def test_todo_page_view(self):
        """
        Test rendering the TODO page
        """
        user = User(username='test_user', password='password')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(username='test_user', password='password', remember=True),
                follow_redirects=True
            )
            response = self.client.get(url_for('todo.todo_list'), follow_redirects=True)
            assert response.status_code == 200
            self.assertIn(b'TODO', response.data)


if __name__ == "__main__":
    unittest.main()