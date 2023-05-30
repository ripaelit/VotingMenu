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
    GET /api/menus/:id/

    list:
    Return a list of all the existing Menu instances.
    GET /api/menus/
    - Filter: Admin can read all menus
    - Filter: Restaurant manager can read all menus of his restaurant.
    - Filter: Employees can read all menus of today (for vote) and past (for reference)

    create:
    Create a new Menu instance.
    POST /api/menus/
    - Only restaurant owner (or admin) can create a menu for a specific restaurant. Otherwise 400 Bad Request with the reason in response body.
    - At most one menu can be created for a restaurant for a specific day. (of today or future) Otherwise 400 Bad Request with the reason in response body.

    update:
    Update an existing Menu instance.
    PUT|PATCH /api/menus/:id/
    - Only restaurant owner (or admin) can update the menu of the restaurant (of today or future).
    - No one can fix the date of menu. Otherwise 400 Bad Request with the reason in response body.


    destroy:
    Delete the specified Menu instance.
    DELETE /api/menus/:id/
    - Only restaurant owner (or admin) can delete the menu of the restaurant (of today or future). Otherwise 400 Bad Request with the reason in response body.
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
    GET /api/restaurants/:id/

    list:
    Return a list of all the existing Restaurant instances.
    GET /api/restaurants/

    create:
    Create a new Restaurant instance.
    POST /api/restaurants/
    - When a user other than administrator attempts to create restaurant, it should return 400 bad request. Reason: "Only administrator user can create restaurants."

    update:
    Update an existing Restaurant instance.
    PUT|PATCH /api/restaurants/:id/
    - no two restaurant can have same (name, location)
    - Only administrator or the manage of the restuarant can update.

    destroy:
    Delete the specified Restaurant instance.
    DELETE /api/restaurants/:id/
    - Only administrator can delete restaurants. Related menus and votes will be deleted (CASCADE)
    - When a user other than administrator attempts to delete restaurant, it should return 400 bad request. Reason: "Only administrator can delete restaurants."
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
