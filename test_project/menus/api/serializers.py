from rest_framework import serializers

from test_project.menus.models import Restaurant, Menu
from test_project.votes.api.serializers import VoteSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    vote_sum = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "content", "restaurant", "vote_sum"]

    def get_restaurant(self, obj, *args, **kwargs):
        from test_project.menus.api.serializers import RestaurantSerializer

        return {
            key: RestaurantSerializer(obj.restaurant, context=self.context).data[key]
            for key in ("name", "location")
        }

    def get_vote_sum(self, obj, *args, **kwargs):
        vote_set = obj.vote_set.all()
        value = 0
        for vote in vote_set:
            value += int(vote.value)
        return value
