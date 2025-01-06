import server


def test_book_valid(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste le cas où le club et la compétition sont valides.
    """
    competition = make_competition()
    club = make_club()
    app_with_data(competition, club)
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )

    response = client.get(
        f"/book/{competition['name']}/{club['name']}"
    )
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "Club test" in decoded_response
    assert "competition test" in decoded_response


def test_book_invalid_club(
        make_competition,
        mocker,
        app_with_data,
        client
):
    """
    Teste le cas où le club est invalide.
    """
    competition = make_competition()
    club = {"name": "InvalidClub"}
    app_with_data(competition, club)
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        side_effect=server.NameNotFound(
            "Nom du Club introuvable. Veuillez réessayer."
        )
    )

    response = client.get(f"/book/{competition['name']}/{club['name']}")
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 404
    assert "Nom du Club introuvable. Veuillez réessayer." in decoded_response


def test_book_invalid_competition(
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste le cas où la compétition est invalide.
    """
    competition = {"name": "InvalidClub"}
    club = make_club()
    app_with_data(competition, club)
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch("server.get_club", return_value=club)
    mocker.patch(
        "server.get_competition",
        side_effect=server.CompetitionNotFound(
            "Compétition introuvable. Veuillez réessayer."
        )
    )

    response = client.get(f"/book/{competition['name']}/{club['name']}")
    decoded_response = response.data.decode("utf-8")

    assert response.status_code == 404
    assert "Compétition introuvable. Veuillez réessayer." in decoded_response
