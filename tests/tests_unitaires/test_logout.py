def test_log_out(client):
    """Test la route logout."""
    response = client.get('/logout')
    assert response.status_code == 302
