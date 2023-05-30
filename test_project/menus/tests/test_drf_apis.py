import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from rest_framework import status

from test_project.users.models import User

pytestmark = pytest.mark.django_db


class TestRestaurantAPI:
    def test_create(self, client: Client, staff_user, restaurant_manager, employee):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "name": "Cake Restaurant",
                "location": "Salman Street 2." 
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.post(
            reverse("api:restaurant-list"),
            data={
                "name": "Cake Restaurant",
                "location": "Salman Street 2." 
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(staff_user)
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

    def test_update(self, client: Client, staff_user, restaurant_manager, employee, ready_restaurant):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.patch(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "name": ready_restaurant.name,
                    "location": ready_restaurant.location
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.patch(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "name": ready_restaurant.name,
                    "location": ready_restaurant.location
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK
        client.force_login(staff_user)
        response = client.patch(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "name": ready_restaurant.name,
                    "location": ready_restaurant.location
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client: Client, staff_user, restaurant_manager, employee, ready_restaurant):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(staff_user)
        response = client.delete(
            reverse("api:restaurant-detail", kwargs={'pk': ready_restaurant.pk}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestMenuAPI:
    def test_create(self, client: Client, staff_user, restaurant_manager, employee, ready_restaurant):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.post(
            reverse("api:menu-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.post(
            reverse("api:menu-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        client.force_login(staff_user)
        response = client.post(
            reverse("api:menu-list"),
            data={
                "restaurant": ready_restaurant.pk,
                "content": "bread, cake"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, client: Client, staff_user, restaurant_manager, employee, ready_menu, ready_restaurant):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.patch(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "content": "bread, cake",
                    "restaurant": ready_restaurant.pk
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.patch(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "content": "bread, cake",
                    "restaurant": ready_restaurant.pk
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK
        client.force_login(staff_user)
        response = client.put(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "content": "bread, cake",
                    "restaurant": ready_restaurant.pk
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client: Client, staff_user, restaurant_manager, employee, ready_menu):
        client.force_login(employee)
        client.defaults["HTTP_API_VERSION"] = "v1"
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        client.force_login(staff_user)
        response = client.delete(
            reverse("api:menu-detail", kwargs={'pk': ready_menu.pk}),
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
