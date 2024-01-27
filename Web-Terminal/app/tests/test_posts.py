from flask                 import url_for
from app.tests.conftest    import client, init_database, log_in_default_user
from ..bundle.posts.models import Post, EnumPriority


def test_post_model():
    post = Post(title='Super post', text='Super context')
    assert post.title == 'Super post'
    assert post.text == 'Super context'


def test_post_get(init_database):
    number_of_posts = Post.query.count()
    assert number_of_posts == 2


def test_post_create(client, init_database, log_in_default_user, tags, category):
    data = {
        'title':   'Example',
        'text':    'Example',
        'type':    'Medium',
        'enabled':  False,
        'category': 1,
        'tag':     [tags[0].id, tags[1].id],
    }
    response = client.post(url_for('posts.create_post'), data=data, follow_redirects=True)
    post = Post.query.filter_by(title='Example').first()
    assert post
    assert post.title == 'Example'
    assert response.status_code == 200


def test_post_view(client, init_database, log_in_default_user, tags):
    data = {
        'title':   'Sample post',
        'text':    'Sample text',
        'type':    'Low',
        'enabled':  False,
        'category': 1,
        'tag':     [tags[0].id, tags[1].id],
    }
    response = client.post(url_for('posts.create_post'), data=data, follow_redirects=True)
    create_post = Post.query.filter_by(title='Sample post').first()
    response = client.post(url_for('posts.view_post', id=create_post.id), follow_redirects=True)
    view_post = Post.query.get(create_post.id)
    assert view_post
    assert view_post.title == 'Sample post'
    assert view_post.text  == 'Sample text'
    assert view_post.type  == EnumPriority.Low
    assert response.status_code == 200


def test_post_update(client, init_database, log_in_default_user, tags):
    data = {
        'title':   'Example',
        'text':    'Example',
        'type':    'Medium',
        'enabled':  False,
        'category': 1,
        'tag':     [tags[0].id, tags[1].id],
    }
    response = client.post(url_for('posts.create_post'), data=data, follow_redirects=True)
    create_post = Post.query.filter_by(title='Sample post').first()
    update_data = {
        'title':   'New example',
        'text':    'New example',
        'type':    'Low',
        'category': 1
    }
    response = client.post(url_for('posts.update_post', id=create_post.id), data=update_data, follow_redirects=True)
    updated_post = Post.query.get(create_post.id)
    assert updated_post
    assert updated_post.title   == 'New example'
    assert updated_post.text    == 'New example'
    assert updated_post.type    == EnumPriority.Low
    assert response.status_code == 200


def test_post_delete(client, init_database, log_in_default_user):
    response = client.get(
        url_for('posts.delete_post', id=1),
        follow_redirects=True
    )
    post = Post.query.filter_by(id=1).first()
    assert response.status_code == 200
    assert post is None
