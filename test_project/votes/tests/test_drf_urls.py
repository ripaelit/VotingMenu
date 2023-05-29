import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_vote_list():
    assert reverse("api:vote-list") == "/api/votes/"
    assert resolve("/api/votes/").view_name == "api:vote-list"


def test_vote_detail():
    vote_pk = 1
    assert (
        reverse("api:vote-detail", kwargs={"pk": vote_pk})
        == f"/api/votes/{vote_pk}/"
    )
    assert resolve(f"/api/votes/{vote_pk}/").view_name == "api:vote-detail"


def test_vote_menu():
    assert (
        reverse("api:vote-vote-menu")
        == f"/api/votes/vote_menu/"
    )
    assert resolve(f"/api/votes/vote_menu/").view_name == "api:vote-vote-menu"
