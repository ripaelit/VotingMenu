from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from test_project.users.models import User
from test_project.utils.models import TimeStampedModel

# Create your models here.
class Restaurant(TimeStampedModel):
    manager = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Name of Restaurant"), max_length=255)
    location = models.CharField(_("Location of Restaurant"), max_length=255)

    def __str__(self) -> str:
        return f"{self.name} located in {self.location}"

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_read_permission(cls, request):
        return True

    @classmethod
    def has_write_permission(cls, request):
        return True

    @classmethod
    def has_create_permission(cls, request):
        return request.user.is_staff

    def has_object_read_permission(self, request):
        return True

    def has_object_write_permission(self, request):
        try:
            Restaurant.objects.get(
                name=request.data.get("name"),
                location=request.data.get("location")
            )
            return False
        except Restaurant.DoesNotExist:
            return True

    def has_object_update_permission(self, request):
        if request.user.is_staff or request.user == self.manager:
            return True
        return False

    def has_object_delete_permission(self, request):
        return request.user.is_staff


class Menu(TimeStampedModel):
    restaurant = models.ForeignKey("menus.Restaurant", on_delete=models.CASCADE)
    content = models.TextField(_("Content of Menu - Menu Items as Plain Text")) # will convert into independent model in later versions

    def __str__(self) -> str:
        return f"{self.restaurant.name} Menu"

    # BEGIN of PERMISSION LOGIC =============
    @classmethod
    def has_read_permission(cls, request):
        return True

    @classmethod
    def has_write_permission(cls, request):
        return True

    @classmethod
    def has_create_permission(cls, request):
        restaurant = Restaurant.objects.get(pk=int(request.data.get("restaurant")))
        if request.user.is_staff or request.user == restaurant.manager:
            today = datetime.now().date()
            create_time = datetime.combine(today, datetime.min.time())
            menus = Menu.objects.filter(
                restaurant=restaurant, created_at__gt=create_time
            )
            if len(menus) > 0:
                return False
            return True
        return False

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        if request.user.is_staff or request.user == self.restaurant.manager:
            return True
        return False

    def has_object_delete_permission(self, request):
        if request.user.is_staff or request.user == self.restaurant.manager:
            return True
        return False
