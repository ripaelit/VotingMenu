from rest_framework import serializers

from test_project.menus.models import Restaurant, Menu
from test_project.votes.api.serializers import VoteSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    vote_set = VoteSerializer(many=True, read_only=True)
    restaurant = serializers.SerializerMethodField()
    _vote = serializers.CharField(read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "content", "restaurant", "_vote", "vote_set"]

    def get_restaurant(self, obj, *args, **kwargs):
        from test_project.menus.api.serializers import RestaurantSerializer

        return {
            key: RestaurantSerializer(obj.restaurant, context=self.context).data[key]
            for key in ("name", "location")
        }
