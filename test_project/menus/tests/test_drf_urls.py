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
