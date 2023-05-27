import pytest

from test_project.users.models import User
from test_project.users.tests.factories import UserFactory
from test_project.menus.models import Menu, Restaurant
from test_project.menus.tests.factories import MenuFactory, RestaurantFactory


class FixtureDataPool:
    menus: list[Menu] = []

    def __init__(self, menus) -> None:
        self.menus = menus


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def restaurant() -> Restaurant:
    restaurant = RestaurantFactory()
    return restaurant


@pytest.fixture
def menu() -> Menu:
    menu = MenuFactory()
    return menu


@pytest.fixture
def ready_user() -> User:
    user = UserFactory(name="test")
    user.save()
    return user


@pytest.fixture
def ready_restaurant() -> Restaurant:
    restaurant = RestaurantFactory(
        name="Cake Restaurant",
        location="Salman Street 3.",
    )
    restaurant.save()
    return restaurant


@pytest.fixture
def ready_menu(ready_restaurant) -> Menu:
    menu = MenuFactory(
        restaurant=ready_restaurant,
        content="Al dente, Blanch, Braise, Caramelise, Dust, Fold, Julienne",
    )
    menu.save()
    return menu


@pytest.fixture
def ready_menus(ready_menu) -> FixtureDataPool:
    result = []
    result.append(ready_menu)
    test_data_pool = FixtureDataPool(result)
    return test_data_pool
