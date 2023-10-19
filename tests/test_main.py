import random
import string
from copy import copy

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = None


def generate_random_username():
    length = random.randint(6, 11)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_password():
    length = random.randint(6, 11)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


random_username = generate_random_username()
random_password = generate_random_password()
test_acc_one_random_instance_with_data = {
    "username": random_username,
    "password": random_username,
    "personal_data": ""
}

# Leaving this for future purpose, can remove
# @pytest.fixture
# def user_data():
#     return {
#         "username": "testuser",
#         "password": "testpassword",
#         "personal_data": ""
#     }


@pytest.fixture
def site_data():
    return {
        "url": "https://example.com",
        "follow_counter": 0
    }


def test_user_registration():
    response = client.post("/register/", json=test_acc_one_random_instance_with_data)
    assert response.status_code == 200
    assert response.json().get("user") is not None


def test_user_login():
    test_acc_one_random_instance_logpass = copy(test_acc_one_random_instance_with_data)
    test_acc_one_random_instance_logpass.pop("personal_data", None)

    response = client.post(
        "/login/",
        json=test_acc_one_random_instance_logpass
    )
    if response.status_code == 200:
        global token
        token = response.json().get("token")
    assert token is not None


def test_site_creation(site_data):
    print(token)
    query_params = {"token": token}
    response = client.post("/create_site", params=query_params, json=site_data)
    print(site_data)
    print(response.status_code)
    print(response.content)

    assert response.status_code == 200
    assert response.json().get("url") == site_data["url"]


def test_dynamic_get_route():
    # Implement the test for the dynamic GET route here
    pass


def test_dynamic_post_route():
    # Implement the test for the dynamic POST route here
    pass


def test_dynamic_patch_route():
    # Implement the test for the dynamic PATCH route here
    pass


def test_dynamic_put_route():
    # Implement the test for the dynamic PUT route here
    pass


def test_dynamic_delete_route():
    # Implement the test for the dynamic DELETE route here
    pass
