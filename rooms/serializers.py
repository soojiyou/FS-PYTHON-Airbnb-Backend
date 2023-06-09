from rest_framework import serializers
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class TinyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "name",
            "price",
        )


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description", "pk")


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True,)
    category = CategorySerializer(read_only=True,)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        if request:
            return room.owner == request.user
        return False

    def get_is_liked(self, room):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Wishlist.objects.filter(user=request.user, rooms__id=room.pk).exists()
        return False


class UserRoomSerializer(serializers.ModelSerializer):
    total_amenities = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
            "rooms",
            "toilets",
            "description",
            "address",
            "pet_friendly",
            "kind",
            "total_amenities",
            "total_reviews",
            "rating",
        )

        def get_total_amenities(self, room):
            return room.total_amenities()

        def get_total_reviews(self, room):
            return room.total_reviews()

        def get_rating(self, room):
            return room.rating()
