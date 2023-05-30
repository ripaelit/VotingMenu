from django.contrib.admin.decorators import register
from django.contrib.admin.options import ModelAdmin

from test_project.menus.models import Restaurant, Menu

# Register your models here.
@register(Restaurant)
class RestaurantAdmin(ModelAdmin):
    list_display = ["name", "location", "manager"]
    search_fields = ["name", "location", "manager"]


@register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ["restaurant", "content"]
    search_fields = ["restaurant", "content"]
