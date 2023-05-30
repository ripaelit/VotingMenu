import pytest

from test_project.menus.tests.factories import MenuFactory, RestaurantFactory

pytestmark = pytest.mark.django_db


class TestMenuFactory:
    def test_create(self):
        menu = MenuFactory()
        assert menu.restaurant


class TestReataurantFactory:
    def test_create(self):
        restaurant = RestaurantFactory()
        assert restaurant.name
