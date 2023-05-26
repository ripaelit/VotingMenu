from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from test_project.utils.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    """
    Default custom user model for Test Project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), max_length=255)
    first_name = models.CharField(_("Firstname of User"), blank=True, max_length=255)
    last_name = models.CharField(_("Lastname of User"), blank=True, max_length=255)

    class PermissionChoices(models.TextChoices):
        Admin = "admin"
        Restaurant = "restaurant"
        Employee = "employee"

    permission_role = models.CharField(
        max_length=100,
        choices=PermissionChoices.choices,
        default=PermissionChoices.Employee,
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_write_permission(cls, request):
        return True
