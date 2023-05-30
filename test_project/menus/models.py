import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from test_project.utils.models import TimeStampedModel

# Create your models here.
class Restaurant(TimeStampedModel):
    manager = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(_("Name of Restaurant"), max_length=255)
    location = models.CharField(_("Location of Restaurant"), max_length=255)

    class Meta:
        unique_together = ('name', 'location')

    history = HistoricalRecords()

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

    def has_object_update_permission(self, request):
        if request.user.is_staff or request.user == self.manager:
            return True
        return False

    def has_object_destroy_permission(self, request):
        return request.user.is_staff


class Menu(TimeStampedModel):
    restaurant = models.ForeignKey("menus.Restaurant", on_delete=models.CASCADE)
    content = models.TextField(_("Content of Menu - Menu Items as Plain Text")) # will convert into independent model in later versions
    date = models.DateField(_("The Date of the Menu"), null=True, blank=True)

    history = HistoricalRecords()

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
        if not request.data.get("restaurant"):
            return False
        restaurant = Restaurant.objects.get(pk=int(request.data.get("restaurant")))
        if not request.user.is_staff and not request.user == restaurant.manager:
            return False
        date = datetime.datetime.strptime(request.data.get("date"), '%Y-%m-%d').date()
        today = datetime.date.today()
        if date < today:
            return False
        if Menu.objects.filter(restaurant=restaurant, date=date).count() > 0:
            return False
        return True

    def has_object_read_permission(self, request):
        return True

    def has_object_update_permission(self, request):
        if request.user.is_staff or request.user == self.restaurant.manager:
            return True
        return False

    def has_object_destroy_permission(self, request):
        if request.user.is_staff or request.user == self.restaurant.manager:
            return True
        return False
