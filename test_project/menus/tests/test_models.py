import pytest
from test_project.votes.models import Vote

pytestmark = pytest.mark.django_db


class TestMenuModel:
    def test_vote_menu(self, ready_user, ready_menu):
        try:
            ready_menu.vote_menu(user=ready_user, menu=ready_menu, value=Vote.VoteValue.BEST)
        except:
            import sys

            _, exception_val, _ = sys.exc_info()
            print(exception_val)
            assert False, "menu.vote_menu() fails"
