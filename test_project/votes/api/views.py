from dry_rest_permissions.generics import DRYPermissions
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from ..models import Vote
from .serializers import VoteSerializer

class VoteViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        SearchFilter,
    ]
    filter_fields = {
        "value": ["exact", "in"],
        "menu__restaurant__name": ["exact", "in"],
    }
    ordering_fields = [
        "value",
        "menu__restaurant__name",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "value",
        "menu__restaurant__name",
    ]
