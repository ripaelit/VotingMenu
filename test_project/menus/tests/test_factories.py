import pytest

from test_project.menus.tests.factories import MenuFactory

pytestmark = pytest.mark.django_db


class TestMenuFactory:
    def test_create(self):
        menu = MenuFactory()
        assert menu.restaurant
