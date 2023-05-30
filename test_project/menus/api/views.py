from django.db.models import Sum
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.filters import BaseFilterBackend, SearchFilter
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from test_project.menus.models import Restaurant, Menu
from .serializers import MenuSerializer, RestaurantSerializer


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


class MenuViewSet(ModelViewSet):
    """
    API:
        update: 
            description: upload menu for restaurant
            user permission role: admin or restaurant
        list: 
            description: get current day menu & get results for current day
            user permission role: everyone
    """
    permission_classes = (DRYPermissions,)
    serializer_class = MenuSerializer
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
    API:
        create:
            description: create restaurant
            permission: admin
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
