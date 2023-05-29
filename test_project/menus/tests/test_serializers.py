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
    def test_serializers(self, ready_restaurant):
        menu_data = {
            "id": ready_restaurant.pk,
            "restaurant": ready_restaurant,
            "content": "Al dente, Blanch, Braise, Caramelise, Dust, Fold, Julienne",
            "vote_sum": 0,
        }
        serializer = MenuSerializer(data=menu_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            print(err)
        assert serializer.is_valid()
