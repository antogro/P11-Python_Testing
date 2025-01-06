from server import (
        get_club,
        load_clubs,
        EmailNotFound,
        NameNotFound,
        EmptyInput
)
import pytest
import json


def test_get_club_email_should_return_club_with_valide_data(
    mocker,
    base_club,
):
    mock_clubs = [base_club]
    mocker.patch("server.clubs", mock_clubs)
    result = get_club(email=base_club["email"])

    assert result == base_club


def test_get_club_name_should_return_club_with_valide_data(
    mocker,
    base_club,
):
    mock_clubs = [base_club]
    mocker.patch("server.clubs", mock_clubs)
    result = get_club(name=base_club["name"])
    assert result == base_club


def test_get_club_should_return_EmptyInput_error_with_no_input(mocker):
    mocker.patch("server.load_clubs", return_value=[])
    with pytest.raises(EmptyInput, match="Veuillez remplir le formulaire."):
        get_club()


def test_get_club_email_should_raise_error_with_invalide_data(
        mocker,
        base_club
):
    mocker.patch("server.load_clubs", return_value=[])
    with pytest.raises(
        EmailNotFound, match="Email du Club introuvable. Veuillez reessayer."
    ):
        get_club(email=base_club["email"])


def test_get_club_name_should_raise_error_with_invalide_data(
        mocker,
        base_club
):
    mocker.patch("server.load_clubs", return_value=[])
    with pytest.raises(
        NameNotFound, match="Nom du Club introuvable. Veuillez reessayer."
    ):
        get_club(name=base_club["name"])


def test_load_club_should_return_data(mocker, base_club):
    mock_club_data = {"clubs": [base_club]}
    mocker.patch("json.load", return_value=mock_club_data)
    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(mock_club_data))
    )
    result = load_clubs()
    assert result == mock_club_data["clubs"]
