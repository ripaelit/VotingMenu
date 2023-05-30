from django.db.models import Sum
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.filters import BaseFilterBackend, SearchFilter
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from test_project.menus.models import Restaurant, Menu
from .serializers import MenuSerializer, RestaurantSerializer
from test_project.utils.viewset_helpers import SerializerFindMixin

class CustomMenuFilterBackend(BaseFilterBackend):
    """
    Filter Backend for MenuViewSet
    """
    def filter_queryset(self, request, queryset, view):
        query_dict = request.query_params.dict()
        queryset = queryset.annotate(
            vote_sum=Sum("vote__value"),
        )

        if query_dict.get("ordering"):
            ordering = query_dict.get("ordering")
            queryset = queryset.order_by(ordering)
        return queryset


class MenuViewSet(SerializerFindMixin, ModelViewSet):
    """
    retrieve:
    Return the specified Menu instance.

    list:
    Return a list of all the existing Menu instances.

    create:
    Create a new Menu instance.

    update:
    Update an existing Menu instance.

    destroy:
    Delete the specified Menu instance.
    """
    permission_classes = (DRYPermissions,)
    queryset = Menu.objects.all()
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        SearchFilter,
        CustomMenuFilterBackend,
    ]
    filter_fields = {
        "content": ["exact", "in"],
        "restaurant__name": ["exact", "in"],
        "restaurant__location": ["exact", "in"],
    }
    ordering_fields = [
        "restaurant__name",
        "restaurant__location",
        "restaurant__created_at",
        "restaurant__updated_at",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "content",
        "restaurant__name",
        "restaurant__location",
    ]


class RestaurantViewSet(ModelViewSet):
    """
    retrieve:
    Return the specified Restaurant instance.

    list:
    Return a list of all the existing Restaurant instances.

    create:
    Create a new Restaurant instance.

    update:
    Update an existing Restaurant instance.

    destroy:
    Delete the specified Restaurant instance.
    """
    permission_classes = (DRYPermissions,)
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        SearchFilter,
    ]
    filter_fields = {
        "manager": ["exact", "in"],
        "name": ["exact", "in"],
        "location": ["exact", "in"],
    }
    ordering_fields = [
        "manager",
        "name",
        "location",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "manager",
        "name",
        "location",
    ]
