from django.db import models
from django.utils.translation import gettext_lazy as _

from test_project.users.models import User
from test_project.votes.models import Vote
from test_project.utils.models import TimeStampedModel
from test_project.utils.permission_mixins import check_permission_role

# Create your models here.
class Restaurant(TimeStampedModel):
    name = models.CharField(_("Name of Restaurant"), max_length=255)
    location = models.CharField(_("Location of Restaurant"), max_length=255)

    def __str__(self) -> str:
        return f"{self.name} located in {self.location}"

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_create_permission(cls, request):
        if request.user.permission_role == User.PermissionChoices.Admin:
            return True
        else:
            return False

    @classmethod
    def has_read_permission(cls, request):
        return True


class Menu(TimeStampedModel):
    restaurant = models.ForeignKey(
        "menus.Restaurant",
        unique=True,
        error_messages={
            "unique": _("The restaurant already has menu."),
        },
        on_delete=models.CASCADE,
    )
    content = models.TextField(_("Content of Menu - Menu Items as Plain Text"))

    def __str__(self) -> str:
        return f"{self.restaurant.name} Menu"

    @classmethod
    def vote_menu(cls, user, menu, value):
        vote = Vote()
        vote.user = user
        vote.menu = menu
        vote.value = value
        vote.save()

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_create_permission(cls, request):
        return request.user.is_authenticated

    @classmethod
    def has_write_permission(cls, request):
        return request.user.is_authenticated

    @classmethod
    def has_read_permission(cls, request):
        return request.user.is_authenticated

    @classmethod
    def has_object_read_permission(cls, request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return check_permission_role(request, self.restaurant)

    def has_object_update_permission(self, request):
        return check_permission_role(request, self.restaurant)

    @classmethod
    def has_vote_menu_permission(cls, request):
        return True

    @classmethod
    def has_object_vote_menu_permission(cls, request):
        return True
