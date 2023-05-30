from django.contrib.admin.decorators import register
from django.contrib.admin.options import ModelAdmin

from .models import Vote

# Register your models here.
@register(Vote)
class VoteAdmin(ModelAdmin):
    list_display = ["menu", "user", "value", "created_at"]
    search_fields = ["menu", "user", "value", "created_at"]
