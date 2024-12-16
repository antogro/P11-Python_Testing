import pytest
import sys
import os
import json

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
    with pytest.raises(EmailNotFound, match='Club introuvables. Veuillez reessayer.'):
        get_club("test2@testgetclub.co")


def test_load_club_should_return_data(mocker):
    mock_data = {
        "clubs": [{
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
        ]
    }
    mocker.patch('json.load', return_value=mock_data)
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_data)))
    result = load_clubs()
    assert result == mock_data['clubs']


def test_load_club_with_file_not_found(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        load_clubs()
