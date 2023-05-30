import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from django.urls import reverse
from rest_framework import status

from test_project.conftest import FixtureDataPool
from test_project.votes.models import Vote

pytestmark = pytest.mark.django_db


class TestVoteAPI:
    def test_create(self, client: Client, staff_user, restaurant_manager, employee, ready_menu):
        client.force_login(employee)
        client.defaults["Api-version"] = "v1"
        response = client.post(
            reverse("api:vote-list"),
            data={
                "menu": ready_menu.pk,
                "value": Vote.VoteValue.BEST
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("menu") == ready_menu.pk
        assert response.data.get("value") == Vote.VoteValue.BEST
        client.force_login(restaurant_manager)
        response = client.post(
            reverse("api:vote-list"),
            data={
                "menu": ready_menu.pk,
                "value": Vote.VoteValue.BEST
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(staff_user)
        response = client.post(
            reverse("api:vote-list"),
            data={
                "menu": ready_menu.pk,
                "value": Vote.VoteValue.BEST
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete(self, client: Client, staff_user, restaurant_manager, employee, ready_vote):
        client.force_login(employee)
        client.defaults["Api-version"] = "v1"
        response = client.delete(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.delete(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(staff_user)
        response = client.delete(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update(self, client: Client, staff_user, restaurant_manager, employee, ready_vote):
        client.force_login(employee)
        client.defaults["Api-version"] = "v1"
        response = client.patch(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "value": Vote.VoteValue.BEST
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(restaurant_manager)
        response = client.patch(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "value": Vote.VoteValue.BEST
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        client.force_login(staff_user)
        response = client.patch(
            reverse("api:vote-detail", kwargs={'pk': ready_vote.pk}),
            data=encode_multipart(
                BOUNDARY,
                {
                    "value": Vote.VoteValue.BEST
                }
            ),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_vote_menu(self, client: Client, staff_user, ready_menus: FixtureDataPool):
        client.force_login(staff_user)
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
