import sys
import os
import pytest


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)

from server import app
from datetime import datetime, timedelta


@pytest.fixture
def base_competition():
    """Fixture de base pour une compétition valide dans le future."""
    return {
        "name": "competition test",
        "date": (
            datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
        "numberOfPlaces": 15
    }


@pytest.fixture
def base_club():
    """Fixture de base pour un club valide."""
    return {
        "email": "test@club.co",
        "name": "Club test",
        "points": 15,
    }


@pytest.fixture
def make_competition(base_competition):
    """Fixture pour créer une compétition."""
    def _make_competition(**kwargs):
        competition = base_competition.copy()
        competition.update(kwargs)
        return competition
    return _make_competition


@pytest.fixture
def make_club(base_club):
    """Fixture pour créer un club."""
    def _make_club(**kwargs):
        club = base_club.copy()
        club.update(kwargs)
        return club
    return _make_club


@pytest.fixture
def client():
    """Fixture pour le client de test Flask"""
    app.config["TESTING"] = True
    app.secret_key = 'something_special'
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_with_data(client):
    """Fixture pour configurer l'app avec les données de test"""
    def _configure_app(competition, club):
        app.competition = [competition]
        app.club = [club]
        return app
    return _configure_app
