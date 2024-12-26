import sys
import os
import pytest


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from server import load_competitions, load_clubs, app


@pytest.fixture
def client():
    app.config['testing'] = True
    app.secret_key = 'something_special'
    app.club = load_clubs()
    app.competitions = load_competitions()
    with app.test_client() as client:
        yield client


@pytest.fixture
def competition():
    return {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }


@pytest.fixture
def club():
    return {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }


@pytest.fixture
def club_low_place():
    return {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }


@pytest.fixture
def competition_test():
    return {
        "name": "competition test",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }


@pytest.fixture
def club_test():
    return {
        "name": "Club test",
        "email": "test@test.co.uk",
        "points": "12"
    }


@pytest.fixture
def places():
    return 5


@pytest.fixture
def data(competition, club, places):
    return competition, club, places


@pytest.fixture
def setup_app_test(competition_test, club_test):
    app.competition = [competition_test]
    app.club_test = [club_test]
    yield app


@pytest.fixture
def setup_app(competition, club):
    app.competition = [competition]
    app.club_test = [club]
    yield app


@pytest.fixture
def setup_app_club_low_place(competition, club_low_place):
    app.competition = [competition]
    app.club_test = [club_low_place]
    yield app
