import server


def test_show_summary_valide_email(mocker, client, base_club):
    """Test la route show_summary avec un email valide."""
    mocker.patch('server.get_club', return_value=base_club)
    response = client.post('/show_summary', data={'email': base_club['email']})

    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 200
    assert f'Welcome, {base_club["email"]}' in decoded_response


def test_show_summary_invalide_email(mocker, client, base_club):
    """Test la route show_summary avec un email invalide."""
    mocker.patch(
        'server.get_club',
        side_effect=server.EmailNotFound(
            "Email du Club introuvable. Veuillez reessayer."
            )
    )
    response = client.post('/show_summary', data={'email': base_club['email']})

    decoded_response = response.data.decode('utf-8')

    assert response.status_code == 404
    assert 'Email du Club introuvable. Veuillez reessayer.' in decoded_response


def test_show_summary_with_no_email(mocker, client):
    """Test la route show_summary avec aucun email."""
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
