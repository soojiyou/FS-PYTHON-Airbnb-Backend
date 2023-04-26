from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("user", "payload", "rating",)


# class HostReviewSerializer(serializers.ModelSerializer):
#     user = TinyUserSerializer(read_only=True)
#     owner = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Review
#         fields = ("owner", "user", "payload", "rating",)

#     def get_owner(self, reviews):
#         return reviews.owner_or_hostname()
