from django.contrib.auth import authenticate, get_user_model, login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    retrieve:
    Return the specified User instance.
    GET /api/users/:id/

    list:
    Return a list of all the existing User instances.
    GET /api/users/

    create:
    Create a new User instance.
    POST /api/users/
    - Only admin can create users (via admin page) (no API required now)

    update:
    Update an existing User instance.
    PUT|PATCH /api/users/:id/

    destroy:
    Delete the specified User instance.
    DELETE /api/menus/:id/

    login:
    Authenticate user login
    POST /api/users/login
    - When username and email are not given, it should return ValidationError
    - When username or password is incorrect, it should return 401 Unauthorized with validation error message
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_permissions(self):
        action_name = self.action_map.get(self.request.method.lower())
        if not action_name and self.request.method.lower() == "options":
            action_names = list(self.action_map.values())
            if len(action_names):
                # TODO: LOW-PRIORITY: Ignoring the rest now. (Quick solution) YAGNI
                action_name = action_names[0]
        if action_name in {
            "login",
            "me",
        }:
            return []
        return super().get_permissions()

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """
        Authenticate user login

        params:
            request:
                body:
                    username: name of user(ex: Teofil)
                    email: email of user(ex: ripaelit1111@gmail.com)
                    password: xxxxxxxxxx
        return:
            If username or email is not set, raise ValidationError.
            If username or password is incorrect, return Unauthorized error
            Return user information for valid user
        """
        password = request.data["password"]
        if request.data.get("username"):
            username = request.data["username"]
            user = authenticate(request, username=username, password=password)
        elif request.data.get("email"):
            email = request.data["email"]
            user = authenticate(request, email=email, password=password)
        else:
            raise ValidationError("Username or email is required.")

        if user is not None:
            login(request, user)
            if not request.data.get("remember_me"):
                request.session.set_expiry(0)
                request.session.modified = True
            serializer = UserSerializer(user, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data="The username and/or password you specified are not correct.",
            )
