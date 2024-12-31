from server import get_club, load_clubs, EmailNotFound, NameNotFound
import pytest
import json


def test_get_club_email_should_return_club_with_valide_data(mocker, club_test):
    mock_club_data = [club_test]
    mocker.patch(
        "server.clubs",
        mock_club_data
    )
    result = get_club(email=club_test['email'])

    assert result == club_test


def test_get_club_name_should_return_club_with_valide_data(mocker, club_test):
    mock_club_data = [club_test]

    mocker.patch(
        "server.clubs",
        mock_club_data
    )
    result = get_club(name=club_test['name'])
    assert result == club_test


def test_get_club_email_should_raise_error_with_invalide_data(
        mocker,
        club_test
):
    mocker.patch('server.load_clubs', return_value=[])
    with pytest.raises(
            EmailNotFound,
            match='Email du Club introuvable. Veuillez reessayer.'
    ):
        get_club(email=club_test['email'])


def test_get_club_name_should_raise_error_with_invalide_data(
        mocker,
        club_test
):
    mocker.patch('server.load_clubs', return_value=[])
    with pytest.raises(
            NameNotFound,
            match='Nom du Club introuvable. Veuillez reessayer.'
    ):
        get_club(name=club_test['name'])


def test_load_club_should_return_data(mocker, club_test):
    mock_club_data = {'clubs': [club_test]}
    mocker.patch(
        'json.load',
        return_value=mock_club_data
    )
    mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data=json.dumps(mock_club_data))
    )
    result = load_clubs()
    assert result == mock_club_data['clubs']


def test_load_club_with_file_not_found_should_raise(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        load_clubs()
