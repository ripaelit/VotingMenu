import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.users.models import User
from test_project.users.api.serializers import UserSerializer

pytestmark = pytest.mark.django_db


class TestUserAPI:
    def test_login(self, client: Client, staff_user):
        client.force_login(staff_user)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.post(
            reverse("api:user-login"),
            data={"username": staff_user.username, "password": staff_user.username},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client: Client, staff_user, restaurant_manager, employee):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user",
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(restaurant_manager)
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user"
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(staff_user)
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user",
            },
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
