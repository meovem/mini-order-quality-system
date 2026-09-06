DEMO_USER = {"username": "qa", "password": "qa123"}


def authenticate(username: str, password: str) -> bool:
    return username == DEMO_USER["username"] and password == DEMO_USER["password"]
