def test_purchase_place_with_valide_data(client, data):
    competition, club, places = data

    response = client.post('/purchase_places', data={
        "competition": competition['name'],
        "club": club['name'],
        "places": places
    })

    assert response.status_code == 200
    assert b'Reservation Confirme'


def test_purchase_place_with_invalide_competition(client, places, club):
    competition = {'name': 'Invalid competition'}

    response = client.post(
        '/purchase_places',
        data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        })
    assert response.status_code == 400


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
    assert response.status_code == 400
    assert b'Vous ne pouvez reserver plus que place que celle disponible.'


def test_purchase_place_with_more_than_12_places(
        client,
        setup_app
):
    places = 13
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app.competition[0]['name'],
            'club': setup_app.club[0]['name'],
            'places': places
            }
    )
    assert response.status_code == 400
    assert b'Vous ne pouvez reserver plus de 12 places.'


def test_purchase_place_without_enought_club_point(
        client,
        setup_app_club_low_place
):
    places = 5
    response = client.post(
        '/purchase_places',
        data={
            'competition': setup_app_club_low_place.competitions[0]['name'],
            'club': setup_app_club_low_place.club[0]['name'],
            'places': places
            }
    )
    assert response.status_code == 200
    assert b'Vous ne pouvez reserver plus de places que le club en possedes.'
