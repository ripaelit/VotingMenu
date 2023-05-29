import pytest

from test_project.votes.tests.factories import VoteFactory

pytestmark = pytest.mark.django_db


class TestVoteFactory:
    def test_create(self):
        vote = VoteFactory()
        assert vote.user
