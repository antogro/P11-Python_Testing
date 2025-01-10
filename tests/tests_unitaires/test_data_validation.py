from server import data_validation
from datetime import datetime, timedelta


def test_data_validation_with_valid_data(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec des données valide."""
    competition = make_competition()
    club = make_club()
    app_with_data(competition, club)
    places = 7
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )

    result = data_validation(
            competition,
            club,
            placesRequired=places
        )
    assert result == []


def test_data_validation_with_more_places_than_available(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec plus de places que celles disponibles."""
    competition = make_competition(numberOfPlaces="10")
    club = make_club()
    app_with_data(competition, club)
    places = 11
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )
    result = data_validation(
        competition,
        club,
        placesRequired=places
    )
    assert result == ['Vous ne pouvez réserver plus de places que celles disponibles.']


def test_data_validation_with_past_competition(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec une compétition passée."""
    plast_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    competition = make_competition(date=plast_date)
    club = make_club()
    app_with_data(competition, club)
    places = 11
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )

    result = data_validation(
        competition,
        club,
        placesRequired=places
    )
    assert result == ['Vous ne pouvez réserver des places pour des compétitions passée.']


def test_data_validation_with_more_places_than_club_points(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec plus de places que les points du club."""
    competition = make_competition()
    club = make_club(points=5)
    app_with_data(competition, club)
    places = 6

    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )
    result = data_validation(
        competition,
        club,
        placesRequired=places
    )
    assert result == ['Vous ne pouvez réserver plus de places que vos points disponibles.']


def test_data_validation_with_negative_places(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec un nombre de places négatif."""
    competition = make_competition(numberOfPlaces="10")
    club = make_club()
    app_with_data(competition, club)
    places = -1

    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )

    result = data_validation(
        competition,
        club,
        placesRequired=places
    )
    assert result == ['Vous ne pouvez réserver 0 places.']


def test_data_validation_with_more_than_12_places(
        make_competition,
        mocker,
        make_club,
        app_with_data
):
    """Test data_validation avec plus de 12 places."""
    competition = make_competition()
    club = make_club()
    app_with_data(competition, club)
    places = 13

    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )
    places = 13

    result = data_validation(
        competition,
        club,
        placesRequired=places
    )
    assert result == ['Vous ne pouvez réserver plus de 12 places sur une compétition.']
