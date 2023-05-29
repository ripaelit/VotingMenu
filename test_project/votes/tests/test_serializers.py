import pytest
from rest_framework.exceptions import ValidationError

from test_project.votes.models import Vote
from test_project.votes.api.serializers import VoteSerializer

pytestmark = pytest.mark.django_db


class TestVoteSerializer:
    def test_serializers(self, ready_user, ready_menu):
        restaurant_data = {
            "user": ready_user.pk,
            "menu": ready_menu.pk,
            "value": Vote.VoteValue.BEST
        }
        serializer = VoteSerializer(data=restaurant_data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as err:
            print(err)
        assert serializer.is_valid()
