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


class CustomMenuFilterBackend(BaseFilterBackend):
    """
    Filter Backend for MenuViewSet
    """

    def filter_queryset(self, request, queryset, view):
        query_dict = request.query_params.dict()
        # queryset = queryset.annotate(
        #     _vote=Sum("vote__value"),
        # )

        # if query_dict.get("ordering"):
        #     ordering = query_dict.get("ordering")
            # ordering = ordering.replace("project__", "_")
            # queryset = queryset.order_by("-list")

        return queryset


class MenuViewSet(ModelViewSet):
    permission_classes = (DRYPermissions,)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS + [
        SearchFilter,
        CustomMenuFilterBackend,
    ]
    filter_fields = {
        "list": ["exact", "in"],
        "restaurant__name": ["exact", "in"],
        "restaurant__location": ["exact", "in"],
    }
    ordering_fields = [
        "list",
        "restaurant__name",
        "restaurant__location",
        "restaurant__created_at",
        "restaurant__updated_at",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "list",
        "restaurant__name",
        "restaurant__location",
    ]

    @action(detail=True, methods=["PATCH"])
    def upload_menu(self, request, pk):
        restaurant_menu = Menu.objects.get(pk=pk)
        restaurant_menu.upload_menu(request.data.get("content"))
        return Response(
            data=MenuSerializer(
                restaurant_menu,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"])
    def vote_menu(self, request, pk):
        restaurant_menu = Menu.objects.get(pk=pk)
        version = request.META.get('api-version')
        if version == "v1" or version == None:
            Menu.vote_menu(request.user, restaurant_menu, Vote.VoteValue.BEST)
        elif version == "v2":
            if request.data.get('top') == 'first':
                value = Vote.VoteValue.BEST
            if request.data.get('top') == 'second':
                value = Vote.VoteValue.BETTER
            if request.data.get('top') == 'third':
                value = Vote.VoteValue.GOOD
            Menu.vote_menu(request.user, restaurant_menu, value)

        return Response(
            data=MenuSerializer(
                restaurant_menu,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )


class RestaurantViewSet(ModelViewSet):
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
