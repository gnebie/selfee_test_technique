import pytest
from api.management.commands.create_users import seed_users_from_data
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_seed_users_creates_users():
    data = [
        {"username": "ash", "password": "pikachu"},
        {"username": "misty", "password": "staryu"},
    ]

    result = seed_users_from_data(data)
    assert result["created"] == ["ash", "misty"]
    assert User.objects.filter(username="ash").exists()
    assert User.objects.filter(username="misty").exists()

@pytest.mark.django_db
def test_seed_users_skips_existing():
    User.objects.create_user(username="brock", password="onix")
    data = [
        {"username": "brock", "password": "123"},
        {"username": "jessie", "password": "ekans"},
    ]

    result = seed_users_from_data(data)
    assert result["created"] == ["jessie"]
    assert result["skipped"] == ["brock"]
