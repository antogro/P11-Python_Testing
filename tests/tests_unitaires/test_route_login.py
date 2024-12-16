import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server import load_competitions, load_clubs, app


@pytest.fixture
def client():
    app.config['testing'] = True
    app.secret_key = 'something_special'
    app.club = load_clubs()
    app.competitions = load_competitions()
    with app.test_client() as client:
        yield client


def test_route_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_show_summary_valide_email(client):
    data = {"email": "kate@shelifts.co.uk"}
    response = client.post('/show_summary', data=data)

    assert response.status_code == 200


def test_show_summary_invalide_email(client):
    data = {"email": "test@email.uk"}
    response = client.post('/show_summary', data=data)
    assert response.status_code == 401
    assert b'Club introuvables. Veuillez reessayer.' in response.data


def test_log_out(client):
    response = client.get('/logout')
    assert response.status_code == 302
