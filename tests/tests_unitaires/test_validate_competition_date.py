from datetime import datetime, timedelta
from server import validate_competition_date


def test_validate_competition_date_past():
    """Test la validation d'une date passée"""
    past_date = datetime.now() - timedelta(days=1)
    is_valid, error_message = validate_competition_date(past_date)

    assert not is_valid
    assert error_message == "Vous ne pouvez pas réserver pour une compétition passée."


def test_validate_competition_date_future():
    """Test la validation d'une date future"""
    future_date = datetime.now() + timedelta(days=1)
    is_valid, error_message = validate_competition_date(future_date)

    assert is_valid
    assert error_message == ""
