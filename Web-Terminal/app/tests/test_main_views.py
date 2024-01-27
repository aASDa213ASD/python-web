from flask import url_for


def test_root_page(client):
    response = client.get(url_for('main.root'))
    assert response.status_code == 200
    assert b'jmp 1293' in response.data


def test_whois_page(client, init_database, log_in_default_user):
    response = client.get(url_for('main.whois'))
    assert response.status_code == 200
    assert b'you can find me' in response.data


def test_projects_page(client, init_database):
    response = client.get(url_for('main.projects'))
    assert response.status_code == 200
    assert b'projects' in response.data


def test_skills_page(client, init_database, log_in_default_user):
    response = client.get(url_for('main.skills'))
    assert response.status_code == 200
    assert b'skills' in response.data
