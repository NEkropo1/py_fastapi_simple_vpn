import random

PROXIES = {
    "proxy1": {
        "address": "proxy1.example.com",
        "port": 8000,
        "username": "user1",
        "password": "password1"
    },
    "proxy2": {
        "address": "proxy2.example.com",
        "port": 8000,
        "username": "user2",
        "password": "password2"
    },

}


def select_random_proxy() -> dict:
    return random.choice(list(PROXIES.values()))

