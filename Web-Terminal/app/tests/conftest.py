import pytest
from flask import url_for

from app import create_app, db
from ..bundle.accounts.models import User
from ..bundle.posts.models import Post, Category, Tag
from ..bundle.todo.models import Todo


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture()
def user_test():
    user = User(username='brand_new', password='password')
    return user


@pytest.fixture(scope='module')
def category():
    category = Category(name="Category")
    yield category


@pytest.fixture(scope='module')
def todo():
    todo_1 = Todo(title="Todo 1", description="Todo description 1", status=False)
    todo_2 = Todo(title="Todo 2", description="Todo description 2", status=False)
    todo_list = [todo_1, todo_2]

    yield todo_list


@pytest.fixture(scope='module')
def tags():
    tag_1 = Tag(name="Tag 1")
    tag_2 = Tag(name="Tag 2")
    tags = [tag_1, tag_2]

    yield tags


@pytest.fixture(scope='module')
def posts(category, tags):
    post_1 = Post(title="Example", text='Example', user_id=1, category=category, tags=tags)
    post_2 = Post(title="Example", text='Example', user_id=1, category=category, tags=tags)

    posts = [post_1, post_2]
    yield posts


@pytest.fixture(scope='module')
def init_database(client, category, posts, todo):
    default_user = User(username='patkennedy',  password='123123123')
    db.session.add(default_user)
    db.session.add(category)
    db.session.add(posts[0])
    db.session.add(posts[1])
    db.session.add(todo[0])
    db.session.add(todo[1])
    db.session.commit()
    yield


@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post(url_for('accounts.login'),
        data={'username': 'patkennedy', 'password': '123123123', 'remember': True},
        follow_redirects=True
    )

    yield

    client.get(url_for('accounts.exit'))
