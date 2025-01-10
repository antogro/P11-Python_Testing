from server import load_competitions, get_competition, CompetitionNotFound
import pytest
import json


def test_load_competition_should_return_data(mocker, base_competition):
    """Test le chargement des données de compétition du JSON."""
    mock_competition_data = {"competitions": [base_competition]}
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


def test_get_competition_should_return_data_with_valid_competition(
        mocker,
        base_competition
):
    """Test la récupération des données de compétition."""
    mock_competition_data = [base_competition]
    mocker.patch('server.competitions', mock_competition_data)
    result = get_competition(base_competition['name'])

    assert result == base_competition


def test_get_competition_should_raise_CompetitionNotFound_error_with_invalid(
    mocker
):
    """Test la levée de l'exception CompetitionNotFound."""
    mock_competition = []
    mocker.patch('server.competitions', mock_competition)
    with pytest.raises(
            CompetitionNotFound,
            match="Compétition introuvable. Veuillez réessayer."
    ):
        get_competition('invalidcompetition')
