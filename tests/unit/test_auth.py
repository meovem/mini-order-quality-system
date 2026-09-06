from app.services.auth import authenticate


def test_valid_user_can_login():
    assert authenticate("qa", "qa123") is True


def test_invalid_password_is_rejected():
    assert authenticate("qa", "wrong") is False
