from server import load_competitions, get_competition, CompetitionNotFound
import pytest
import json


def test_load_competition_should_return_data(mocker, competition_test):
    mock_competition_data = {"competitions": [competition_test]}
    mocker.patch(
        'json.load', return_value=mock_competition_data
    )
    mocker.patch(
        'builtins.open',
        mocker.mock_open(
            read_data=json.dumps(mock_competition_data))
    )
    result = load_competitions()
    assert result == mock_competition_data['competitions']


def test_load_competition_with_file_not_found(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        load_competitions()


def test_get_competition_should_return_competition_with_valid_competition(
        mocker,
        competition_test
):
    mock_competition_data = [competition_test]
    mocker.patch('server.competitions', mock_competition_data)
    result = get_competition(competition_test['name'])

    assert result == competition_test


def test_get_competition_should_raise_CompetitionNotFound_error_with_invalid(
    mocker
):
    mock_competition = []
    mocker.patch('server.competitions', mock_competition)
    with pytest.raises(
            CompetitionNotFound,
            match="Compétition introuvable. Veuillez réessayer."
    ):
        get_competition('invalidcompetition')
