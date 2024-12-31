def test_log_out(client):
    response = client.get('/logout')
    assert response.status_code == 302
