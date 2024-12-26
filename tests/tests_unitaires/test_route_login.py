def test_route_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_show_summary_valide_email(client, club):
    data = {"email": club['email']}
    response = client.post('/show_summary', data=data)

    assert response.status_code == 200


def test_show_summary_invalide_email(client, club_test):
    data = {"email": club_test['email']}
    response = client.post('/show_summary', data=data)
    assert response.status_code == 404
    assert b'Club introuvable. Veuillez reessayer.' in response.data


def test_show_summary_with_no_email(client):
    data = {"email": " "}
    response = client.post('/show_summary', data=data)
    assert response.status_code == 404


def test_log_out(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_book(client, competition, club):
    response = client.get(f"/book/{competition['name']}/{club['name']}")
    assert response.status_code == 200
