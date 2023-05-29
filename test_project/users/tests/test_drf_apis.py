import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.users.models import User
from test_project.users.api.serializers import UserSerializer

pytestmark = pytest.mark.django_db


class TestUserAPI:
    def test_login(self, client: Client, ready_user):
        client.force_login(ready_user)
        response = client.post(
            reverse("api:user-login"),
            data={"username": ready_user.username, "password": ready_user.username},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client: Client, ready_user, ready_user1, ready_user2):
        client.force_login(ready_user2)
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user",
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(ready_user1)
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user"
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(ready_user)
        response = client.post(
            reverse("api:user-login"),
            data={"username": ready_user.username, "password": ready_user.username},
        )
        assert response.status_code == status.HTTP_200_OK
