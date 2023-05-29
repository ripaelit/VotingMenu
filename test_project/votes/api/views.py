from dry_rest_permissions.generics import DRYPermissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet

from test_project.menus.models import Menu
from ..models import Vote
from .serializers import VoteSerializer

# We vote top three menus in new version api(v2)
VOTED_MENUS_COUNT_V2 = 3
# We vote only one menu in old version api(v1)
VOTED_MENUS_COUNT_V1 = 1


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
                Vote.create(request.user, restaurant_menu, Vote.VoteValue.BEST)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="We vote only one menu in old version api."
                )
        if version == "v2" or version == None:
            if len(voted_menus_id) == VOTED_MENUS_COUNT_V2:
                menus = []
                for id in voted_menus_id:
                    restaurant_menu = Menu.objects.get(pk=int(id))
                    menus.append(restaurant_menu)
                Vote.create_votes_v2(request.user, menus)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="We vote three menus in new version api."
                )

        return Response(status=status.HTTP_200_OK)
