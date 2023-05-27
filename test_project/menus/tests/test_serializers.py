import pytest
from rest_framework.exceptions import ValidationError

from test_project.menus.api.serializers import MenuSerializer, RestaurantSerializer

pytestmark = pytest.mark.django_db


class TestRestaurantSerializer:
    def test_serializers(self):
        restaurant_data = {
            "name": "Cake Restaurant",
            "location": "Salman Street 3.",
        }
        serializer = RestaurantSerializer(data=restaurant_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            print(err)
        assert serializer.is_valid()


class TestMenuSerializer:
    def test_serializers(self, restaurant):
        menu_data = {
            "restaurant": restaurant.pk,
            "content": "Al dente, Blanch, Braise, Caramelise, Dust, Fold, Julienne",
        }
        serializer = MenuSerializer(data=menu_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            print(err)
        assert serializer.is_valid()
