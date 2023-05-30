from rest_framework import serializers

from test_project.menus.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class MenuDetailSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField(read_only=False, required=False)
    vote_sum = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Menu
        fields = ["id", "content", "restaurant", "vote_sum"]

    def get_restaurant(self, obj, *args, **kwargs):
        from test_project.menus.api.serializers import RestaurantSerializer

        return {
            key: RestaurantSerializer(obj.restaurant, context=self.context).data[key]
            for key in ("name", "location")
        }
