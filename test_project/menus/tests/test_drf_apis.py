import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.conftest import FixtureDataPool

pytestmark = pytest.mark.django_db


class TestMenuAPI:
    @pytest.mark.skip
    def test_vote_menu(self, client: Client, ready_menus: FixtureDataPool):
        response = client.post(
            reverse("api:menu-vote-menu", kwargs={"pk": ready_menus.menus[0].pk}),
            data={"top": "first"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["content"], str)
