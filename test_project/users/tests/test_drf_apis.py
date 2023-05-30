import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.users.models import User
from test_project.users.api.serializers import UserSerializer

pytestmark = pytest.mark.django_db


class TestUserAPI:
    def test_login(self, client: Client, user_with_admin_permission):
        client.force_login(user_with_admin_permission)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:user-login"),
            data={"username": user_with_admin_permission.username, "password": user_with_admin_permission.username},
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user",
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(user_with_restaurant_manager_permission)
        response = client.post(
            reverse("api:user-list"),
            data={
                "name": "new_user"
            }
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        client.force_login(user_with_admin_permission)
        response = client.post(
            reverse("api:user-login"),
            data={"username": user_with_admin_permission.username, "password": user_with_admin_permission.username},
        )
        assert response.status_code == status.HTTP_200_OK
