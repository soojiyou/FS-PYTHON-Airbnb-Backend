from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "is_superuser", "id", "is_staff", "is_active",
                   "first_name", "last_name", "groups", "user_permissions",)


class PublucUserSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    total_rooms = serializers.SerializerMethodField()

    class Meta:
        model = User
        include = ("name",
                   "gender",
                   "avatar",
                   "username",
                   "language",
                   "total_reviews",
                   "total_rooms",)
        # review몇개만 보여주기 가능한지.

    def get_total_reviews(self, user):
        return user.total_reviews()

    def get_total_rooms(self, user):
        return user.total_rooms()
