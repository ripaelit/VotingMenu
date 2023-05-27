import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.conftest import FixtureDataPool

pytestmark = pytest.mark.django_db


class TestMenuAPI:
    def test_vote_menu(self, client: Client, ready_user, ready_menus: FixtureDataPool):
        client.force_login(ready_user)
        response = client.post(
            reverse("api:menu-vote-menu", kwargs={"pk": ready_menus.menus[0].pk}),
            data={"top": "first"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["restaurant"]["name"] == ready_menus.menus[0].restaurant.name
        assert response.data["restaurant"]["location"] == ready_menus.menus[0].restaurant.location
        assert response.data["content"] == ready_menus.menus[0].content
