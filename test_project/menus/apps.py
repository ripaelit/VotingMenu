from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class MenusConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "test_project.menus"
    verbose_name = _("Restaurant and Menu")
