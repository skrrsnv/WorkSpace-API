import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def owner():
    return User.objects.create_user(username="owner", password="pass123")


@pytest.fixture
def admin():
    return User.objects.create_user(username="admin", password="pass123")


@pytest.fixture
def member():
    return User.objects.create_user(username="member", password="pass123")