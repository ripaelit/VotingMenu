from django.db import models
from django.utils.translation import gettext_lazy as _

from test_project.utils.models import TimeStampedModel

# Create your models here.
class Vote(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    menu = models.ForeignKey("menus.Menu", on_delete=models.CASCADE)

    class VoteValue(models.IntegerChoices):
        NORMAL = 0, _("Restaurant is normal (score:0)") # normal -> 0
        GOOD = 1, _("Restaurant is good (score:1)") # good -> 1
        BETTER = 2, _("Restaurant is better (score:2)") # better -> 2
        BEST = 3, _("Restaurant is the best (score:3)") # best -> 3

    value = models.IntegerField(
        _("Vote value"),
        help_text=_("Vote for the restaurant"),
        choices=VoteValue.choices,
        default=VoteValue.NORMAL,
    )

    @classmethod
    def create(cls, user, menu, value):
        try:
            inst = cls.objects.get(user=user)
            return inst
        except cls.DoesNotExist:
            new_inst = cls(user=user, menu=menu)
            new_inst.value = value
            new_inst.save()
            return new_inst

    @classmethod
    def create_votes_v2(cls, user, menus):
        try:
            inst = cls.objects.get(user=user)
            return inst
        except cls.DoesNotExist:
            value = [
                Vote.VoteValue.BEST,
                Vote.VoteValue.BETTER,
                Vote.VoteValue.GOOD,
            ]
            for i in range(len(menus)):
                new_inst = cls(user=user, menu=menus[i])
                new_inst.value = value[i]
                new_inst.save()
            return new_inst

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_create_permission(cls, request):
        return True

    @classmethod
    def has_read_permission(cls, request):
        return True

    @classmethod
    def has_vote_menu_permission(cls, request):
        return True

    @classmethod
    def has_vote_menu_permission(cls, request):
        return True
