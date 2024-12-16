import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from server import load_competitions, get_competition, CompetitionNotFound


def test_load_club_should_return_data(mocker):
    mock_data = {
        "competitions": [
            {
                "name": "testcompetition",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "11"
            }
        ]
    }
    mocker.patch('json.load', return_value=mock_data)
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(mock_data)))
    result = load_competitions()
    assert result == mock_data['competitions']


def test_load_club_with_file_not_found(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        load_competitions()


def test_should_return_competition_with_valid_competition(mocker):
    mock_response = [
        {
            "name": "testcompetition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "11"
        }
    ]
    mocker.patch('server.load_competitions', return_value=mock_response)
    result = get_competition('testcompetition')
    expected_value = {
            "name": "testcompetition",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "11"
        }
    assert result == expected_value


def test_should_raise_CompetitionNotFound_error_with_invalid_competition(mocker):
    mock_response = []
    mocker.patch('server.load_competitions', return_value=mock_response)
    with pytest.raises(CompetitionNotFound, match="Compétition introuvables. Veuillez réessayer."):
        get_competition('invalidcompetition')
