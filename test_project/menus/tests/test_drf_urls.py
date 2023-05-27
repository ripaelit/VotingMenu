import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_menu_list():
    assert reverse("api:menu-list") == "/api/menus/"
    assert resolve("/api/menus/").view_name == "api:menu-list"


def test_menu_detail():
    menu_pk = 1
    assert (
        reverse("api:menu-detail", kwargs={"pk": menu_pk})
        == f"/api/menus/{menu_pk}/"
    )
    assert resolve(f"/api/menus/{menu_pk}/").view_name == "api:menu-detail"


def test_upload_menu():
    menu_pk = 1
    assert (
        reverse("api:menu-upload-menu", kwargs={"pk": menu_pk})
        == f"/api/menus/{menu_pk}/upload_menu/"
    )
    assert resolve(f"/api/menus/{menu_pk}/upload_menu/").view_name == "api:menu-upload-menu"


def test_vote_menu():
    menu_pk = 1
    assert (
        reverse("api:menu-vote-menu", kwargs={"pk": menu_pk})
        == f"/api/menus/{menu_pk}/vote_menu/"
    )
    assert resolve(f"/api/menus/{menu_pk}/vote_menu/").view_name == "api:menu-vote-menu"


def test_restaurant_list():
    assert reverse("api:restaurant-list") == "/api/restaurants/"
    assert resolve("/api/restaurants/").view_name == "api:restaurant-list"


def test_restaurant_detail():
    restaurant_pk = 1
    assert (
        reverse("api:restaurant-detail", kwargs={"pk": restaurant_pk})
        == f"/api/restaurants/{restaurant_pk}/"
    )
    assert resolve(f"/api/restaurants/{restaurant_pk}/").view_name == "api:restaurant-detail"
