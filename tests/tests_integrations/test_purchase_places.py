from datetime import datetime, timedelta


def test_purchase_place_with_valide_data(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste l'achat de places pour une compétition par un club.
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
    places = 4
    response = client.post('/purchase_places', data={
        "competition": competition['name'],
        "club": club['name'],
        "places": places
    })
    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 200
    assert 'Réservation confirmée !' in decoded_response


def test_purchase_place_with_invalide_competition(client, base_club, mocker):
    """
    Teste l'achat de places pour une compétition inexistante.
    """
    competition = {'name': 'Invalid competition'}
    mocker.patch(
        'server.get_club',
        return_value=base_club
    )
    places = 4
    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': base_club['name'],
            'places': places
        })
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert 'Compétition introuvable. Veuillez réessayer.' in decoded_response


def test_purchase_place_with_invalide_club(
        client,
        base_competition,
        mocker
):
    """
    Teste l'achat de places pour un club inexistant.
    """
    club = {'name': 'Invalid club'}
    mocker.patch('server.get_competition', return_value=base_competition)
    places = 4
    response = client.post(
        '/purchase_places',
        data={
            'competition': base_competition['name'],
            'club': club['name'],
            'places': places
        })
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert 'Nom du Club introuvable. Veuillez reessayer.' in decoded_response


def test_purchase_place_with_to_more_place_than_competition_places(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste l'achat de places pour une compétition avec plus de places que
    celles disponibles.
    """
    competition = make_competition(numberOfPlaces="10")
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
    places = 11
    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert ('Vous ne pouvez réserver plus de places que celles disponibles.' in
            decoded_response)


def test_purchase_place_with_more_than_12_places(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste l'achat de places pour une compétition avec plus de 12 places.
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
    places = 13
    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver plus de 12 places sur une compétition.'
        in decoded_response
        )


def test_purchase_place_with_insufficient_club_points(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste l'achat de places pour une compétition avec des points insuffisants
    pour le club.
    """
    competition = make_competition()
    club = make_club(points=5)
    app_with_data(competition, club)
    mocker.patch(
        'server.get_competition',
        return_value=competition
    )
    mocker.patch(
        'server.get_club',
        return_value=club
    )
    places = 6
    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver plus de places que vos points disponibles.'
        in decoded_response
        )


def test_points_deduction_after_purchase(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste la déduction des points après l'achat de places pour une compétition.
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
    places = 7
    response = client.post('/purchase_places', data={
        "competition": competition['name'],
        "club": club['name'],
        "places": places
    })
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 200

    assert 'Réservation confirmée !' in decoded_response
    # Vérification des points.
    assert 'Points available: 8' in decoded_response


def test_purchase_place_with_past_competition(
        make_competition,
        mocker,
        make_club,
        app_with_data,
        client
):
    """
    Teste l'achat de places pour une compétition passée.
    """
    competition = make_competition(date=(
        datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    )
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
    places = 7
    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver des places pour des compétitions passée.'
        in decoded_response
    )
