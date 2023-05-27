from django.db.models import Case, F, Q, Value, When, Sum
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, SearchFilter
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from test_project.menus.models import Restaurant, Menu
from .serializers import MenuSerializer, RestaurantSerializer
from test_project.votes.models import Vote


# We vote top three menus in new version api(v2)
VOTED_MENUS_COUNT_V2 = 3
# We vote only one menu in old version api(v1)
VOTED_MENUS_COUNT_V1 = 1

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
        vote_menu: 
            description: vote for restaurant menu
            user permission role: everyone
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
        "content",
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

    @action(detail=False, methods=["POST"])
    def vote_menu(self, request):
        """
        Vote for menu

        params:
            request:
                header:
                    api-version: version of api(ex: "v1" for old version and "v2" for new version)
                body:
                    menus: id of menus to be voted (ex: "10" in v1, "17,23,34" in v2)

        return: HTTP_200_OK response
        """
        voted_menus_id = request.data.get("menus")
        voted_menus_id = voted_menus_id.split(',')

        version = request.META.get('Api-version')
        if version == "v1":
            if len(voted_menus_id) == VOTED_MENUS_COUNT_V1:
                restaurant_menu = Menu.objects.get(pk=int(voted_menus_id[0]))
                Menu.vote_menu(request.user, restaurant_menu, Vote.VoteValue.BEST)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="We vote only one menu in old version api."
                )
        if version == "v2" or version == None:
            if len(voted_menus_id) == VOTED_MENUS_COUNT_V2:
                value = [
                    Vote.VoteValue.BEST,
                    Vote.VoteValue.BETTER,
                    Vote.VoteValue.GOOD,
                ]
                for i in range(VOTED_MENUS_COUNT_V2):
                    restaurant_menu = Menu.objects.get(pk=int(voted_menus_id[i]))
                    Menu.vote_menu(request.user, restaurant_menu, value[i])
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="We vote three menus in new version api."
                )

        return Response(status=status.HTTP_200_OK)


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
        "name": ["exact", "in"],
        "location": ["exact", "in"],
    }
    ordering_fields = [
        "name",
        "location",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "location",
    ]
