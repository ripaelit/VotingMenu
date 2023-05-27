import factory
import faker
from django.db.models.signals import post_save
from factory import Faker
from factory.django import DjangoModelFactory

from test_project.menus.models import (
    Menu,
    Restaurant,
)

__Faker__ = faker.factory.Factory.create
__fake__ = __Faker__()


@factory.django.mute_signals(post_save)
class RestaurantFactory(DjangoModelFactory):
    name = Faker("name")
    location = Faker("sentence")

    class Meta:
        model = Restaurant


@factory.django.mute_signals(post_save)
class MenuFactory(DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    content = Faker("sentence")

    class Meta:
        model = Menu
