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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["POST"])
    def login(self, request):
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