import server


def test_book_valid(client, competition_test, club_test, mocker):
    """
    Teste le cas où le club et la compétition sont valides.
    """
    mocker.patch("server.get_club", return_value=club_test)
    mocker.patch("server.get_competition", return_value=competition_test)

    response = client.get(
        f"/book/{competition_test['name']}/{club_test['name']}"
    )
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Club test" in decoded_response
    assert "competition test" in decoded_response


def test_book_invalid_club(client, competition_test, mocker):
    """
    Teste le cas où le club est invalide.
    """
    mocker.patch(
        "server.get_club", side_effect=server.NameNotFound(
            "Nom du Club introuvable. Veuillez réessayer."
        )
    )

    response = client.get(f"/book/{competition_test['name']}/InvalidClub")
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 404
    assert "Nom du Club introuvable. Veuillez réessayer." in decoded_response


def test_book_invalid_competition(client, club_test, mocker):
    """
    Teste le cas où la compétition est invalide.
    """
    mocker.patch("server.get_club", return_value=club_test)
    mocker.patch(
        "server.get_competition",
        side_effect=server.CompetitionNotFound(
            "Compétition introuvable. Veuillez réessayer."
        )
    )

    response = client.get(f"/book/InvalidCompetition/{club_test['name']}")
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 404
    assert "Compétition introuvable. Veuillez réessayer." in decoded_response
