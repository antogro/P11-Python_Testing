import pytest
from server import app, load_clubs, load_competitions


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def clubs():
    return load_clubs()


@pytest.fixture
def competitions():
    return load_competitions()


def test_user_flow(client, clubs, competitions):
    # Test show_summary
    response = client.post('/show_summary', data=dict(email=clubs[0]['email']))
    assert response.status_code == 200
    assert f'Welcome, {clubs[0]["email"]}' in response.data.decode('utf-8')

    # Test book
    response = client.get(
        f"/book/{competitions[2]['name']}/{clubs[0]['name']}")
    assert response.status_code == 200
    assert f'{competitions[2]['name']}' in response.data.decode("utf-8")

    # Test purchase_places
    response = client.post('/purchase_places', data=dict(
        competition=competitions[2]['name'],
        club=clubs[0]['name'],
        places=5
    ))
    assert response.status_code == 200
    assert 'Réservation confirmée !' in response.data.decode("utf-8")

    # Test display_points
    response = client.get('/clubs_points')
    assert response.status_code == 200
    assert 'Points des Clubs' in response.data.decode("utf-8")
