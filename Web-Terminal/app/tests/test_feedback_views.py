from flask import url_for


def test_feedback_page(client):
    response = client.get(url_for('feedback.feedback_list'))
    assert response.status_code == 200
    assert b'feedback' in response.data
