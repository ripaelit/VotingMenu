import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from test_project.conftest import FixtureDataPool

pytestmark = pytest.mark.django_db


class TestVoteAPI:
    def test_vote_menu(self, client: Client, ready_user, ready_menus: FixtureDataPool):
        client.force_login(ready_user)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:vote-vote-menu"),
            data={"menus": ready_menus.menus[0].pk}
        )
        assert response.status_code == status.HTTP_200_OK
        menus_id = ','.join([str(menu.pk) for menu in ready_menus.menus])
        response = client.post(
            reverse("api:vote-vote-menu"),
            data={"menus": menus_id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        client.defaults["Api-version"] = "v2"
        response = client.post(
            reverse("api:vote-vote-menu"),
            data={"menus": menus_id}
        )
        assert response.status_code == status.HTTP_200_OK
        menus_id = ','.join([str(menu.pk) for menu in ready_menus.menus[1:]])
        response = client.post(
            reverse("api:vote-vote-menu"),
            data={"menus": menus_id}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
