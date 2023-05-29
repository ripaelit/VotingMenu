import factory
import faker
from django.db.models.signals import post_save
from factory import Faker
from factory.django import DjangoModelFactory

from test_project.votes.models import Vote
from test_project.menus.tests.factories import MenuFactory
from test_project.users.tests.factories import UserFactory

__Faker__ = faker.factory.Factory.create
__fake__ = __Faker__()


@factory.django.mute_signals(post_save)
class VoteFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    menu = factory.SubFactory(MenuFactory)
    value = Faker("pyint", max_value=3)

    class Meta:
        model = Vote
