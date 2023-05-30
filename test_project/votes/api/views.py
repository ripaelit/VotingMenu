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
    """
    retrieve:
    Return the specified User instance.
    GET /api/votes/:id/

    list:
    Return a list of all the existing User instances.
    GET /api/votes/

    create:
    Create a new User instance.
    POST /api/votes/
    - A user can create at most one vote a day. Second attempt should return ValidationError (Django ValidationError)
    - A user can create at most one vote a day. Second attempt should return 400 Bad Request with validation error message.

    update:
    Update an existing User instance.
    PUT|PATCH /api/votes/:id/
    - A user cannot withdraw or update his vote.
    - 400 Bad request. "A user cannot withdraw or update his vote."

    destroy:
    Delete the specified User instance.
    DELETE /api/votes/:id/
    - A user cannot withdraw or update his vote.
    - 400 Bad request. "A user cannot withdraw or update his vote."

    vote_menu:
    Vote for restaurant menu
    POST /api/votes/vote_menu
    - Only employees can vote. (Admin, restaurant managers cannot vote with their names)
    - Vote for a menu should be made in the same date as menu. (00:00~24:00 in server time zone)
    - Vote for a menu should be made in the same date as menu. (00:00~24:00 in server time zone)  Otherwise 400 Bad Request with the reason in response body. ("Too early to vote" "Too late to vote")
    """

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
                    HTTP_API_VERSION: version of api(ex: "v1" for old version and "v2" for new version)
                body:
                    menus: id of menus to be voted (ex: "10" in v1, "17,23,34" in v2)

        return: HTTP_200_OK response
        """
        voted_menus_id = str(request.data.get("menus"))
        voted_menus_id = voted_menus_id.split(',')

        version = request.META.get('HTTP_API_VERSION')
        if version == "v1":
            if len(voted_menus_id) == VOTED_MENUS_COUNT_V1:
                restaurant_menu = Menu.objects.get(pk=int(voted_menus_id[0]))
                Vote.create(request.user, restaurant_menu, Vote.VoteValue.BEST)
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data="We vote only one menu in old version api."
                )
        if version == "v2":
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
