import pytest
from test_project.votes.models import Vote

pytestmark = pytest.mark.django_db


class TestVoteModel:
    def test_vote_menu(self, ready_user, ready_menu, ready_menus):
        try:
            Vote.create(user=ready_user, menu=ready_menu, value=Vote.VoteValue.BEST)
            Vote.create_votes_v2(user=ready_user, menus=ready_menus)
        except:
            import sys

            _, exception_val, _ = sys.exc_info()
            print(exception_val)
            assert False, "menu.vote_menu() fails"
