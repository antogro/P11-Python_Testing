def test_purchase_place_with_valide_data(client, data):
    competition, club, places = data

    response = client.post('/purchase_places', data={
        "competition": competition['name'],
        "club": club['name'],
        "places": places
    })
    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 200
    assert 'Réservation confirmée !' in decoded_response


def test_purchase_place_with_invalide_competition(client, places, club):
    competition = {'name': 'Invalid competition'}

    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        })
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert 'Compétition introuvable. Veuillez réessayer.' in decoded_response


def test_purchase_place_with_invalide_club(client, places, competition):
    club = {'name': 'Invalid club'}

    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        })
    decoded_response = response.data.decode('utf-8')
    print(decoded_response)
    assert response.status_code == 400
    assert 'Nom du Club introuvable. Veuillez reessayer.' in decoded_response


def test_purchase_place_with_to_more_place_than_competition_places(
        client,
        setup_app
):
    places = 15
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app.competition[0]['name'],
            'club': setup_app.club[0]['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert ('Vous ne pouvez réserver plus de places que celles disponibles.' in
            decoded_response)


def test_purchase_place_with_more_than_12_places(
        client,
        setup_app_competition_more_place
):
    places = 13
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app_competition_more_place.competition[0]['name'],
            'club': setup_app_competition_more_place.club[0]['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver plus de 12 places sur une compétition.'
        in decoded_response
        )


def test_purchase_place_with_insufficient_competition_places(client, setup_app):
    places = 14  # Plus que les places disponibles
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app.competition[0]['name'],
            'club': setup_app.club[0]['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver plus de places que celles disponibles.'
        in decoded_response
        )


def test_purchase_place_with_insufficient_club_points(
        client,
        setup_app_club_low_place
):
    places = 6  # Plus que les points disponibles du club
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app_club_low_place.competition[0]['name'],
            'club': setup_app_club_low_place.club_test[0]['name'],
            'places': places
        }
    )
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 400
    assert (
        'Vous ne pouvez réserver plus de places que vos points disponibles.'
        in decoded_response
        )


def test_points_deduction_after_purchase(client, setup_app, data):
    competition, club, places = data

    response = client.post('/purchase_places', data={
        "competition": competition['name'],
        "club": club['name'],
        "places": places
    })
    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 200
    assert 'Réservation confirmée !' in decoded_response

    # Vérification des points.
    assert 'Number of Places: 3' in decoded_response
    assert 'Points available: 2' in decoded_response

