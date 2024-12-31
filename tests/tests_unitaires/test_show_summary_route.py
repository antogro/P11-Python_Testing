import server


def test_show_summary_valide_email(mocker, client, club_test):
    mocker.patch('server.get_club', return_value=club_test)
    data = {"email": club_test['email']}
    response = client.post('/show_summary', data=data)

    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 200
    assert f'Welcome, {club_test["email"]}' in decoded_response


def test_show_summary_invalide_email(mocker, client, club_test):
    mocker.patch(
        'server.get_club',
        side_effect=server.EmailNotFound(
            "Club introuvable. Veuillez reessayer."
            )
    )
    data = {"email": "invalide_email@mail.co"}
    response = client.post('/show_summary', data=data)

    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 404
    assert 'Club introuvable. Veuillez reessayer.' in decoded_response


def test_show_summary_with_no_email(mocker, client):
    mocker.patch(
        'server.get_club',
        side_effect=server.EmptyInput(
            "Veuillez remplir le formulaire."
            )
    )
    data = {"email": ""}
    response = client.post('/show_summary', data=data)

    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 404
    assert 'Veuillez remplir le formulaire.' in decoded_response
