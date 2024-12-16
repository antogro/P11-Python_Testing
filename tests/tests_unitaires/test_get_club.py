import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server import get_club, load_clubs, EmailNotFound


def test_get_club_should_returne_club_with_valide_data(mocker):
    mock_response = [{
        "name": "test1",
        "email": "test@testgetclub.co",
        "points": "13",
    }]
    mocker.patch("server.load_clubs", return_value=mock_response)
    result = get_club("test@testgetclub.co")
    expected_value = {
        "name": "test1",
        "email": "test@testgetclub.co",
        "points": "13"}
    assert result == expected_value


def test_get_club_should_raise_error_with_invalide_data(mocker):

    mocker.patch('server.load_clubs', return_value=[])
    with pytest.raises(EmailNotFound, match='Club introuvables. Veuillez réessayer.'):
        get_club("test2@testgetclub.co")
