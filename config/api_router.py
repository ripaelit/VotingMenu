from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from test_project.users.api.views import UserViewSet
from test_project.votes.api.views import VoteViewSet
from test_project.menus.api.views import RestaurantViewSet, MenuViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls
