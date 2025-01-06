def test_route_index(client):
    response = client.get('/')
    decoded_response = response.data.decode('utf-8')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT Registration Portal!' in decoded_response
