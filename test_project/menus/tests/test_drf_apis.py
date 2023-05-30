import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from rest_framework import status

from test_project.users.models import User

pytestmark = pytest.mark.django_db


class TestRestaurantAPI:
    def test_create(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "name": "Cake Restaurant",
                "location": "Salman Street 2." 
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_restaurant_manager_permission)
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "name": "Cake Restaurant",
                "location": "Salman Street 2." 
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_admin_permission)
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "name": "Cake Restaurant",
                "location": "Salman Street 2." 
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("name") == "Cake Restaurant"
        assert response.data.get("location") == "Salman Street 2."

    def test_delete(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission, ready_restaurant):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_restaurant_manager_permission)
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_admin_permission)
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestMenuAPI:
    def test_create(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission, ready_restaurant):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:menu-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_restaurant_manager_permission)
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_admin_permission)
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission, ready_menu):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.patch(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data={
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_restaurant_manager_permission)
        response = client.patch(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data={
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_admin_permission)
        response = client.put(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "restaurant": ready_menu.restaurant.pk,
                    "content": "bread, cake"
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self, client: Client, user_with_admin_permission, user_with_restaurant_manager_permission, user_with_employee_permission, ready_menu):
        client.force_login(user_with_employee_permission)
        client.defaults["Api-version"] = "v1"
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_restaurant_manager_permission)
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(user_with_admin_permission)
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
