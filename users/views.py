import re
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from . import serializers, models
from rooms.models import Room
from rooms.serializers import RoomListSerializer
from reviews.models import Review
from reviews.serializers import ReviewSerializer  # HostReviewSerializer


class MyProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user, data=request.data, partial=True,)
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        username = request.data.get("username")
        if username == "myprofile":
            raise ("'myprofile' cannot be used for username!")
        password = request.data.get("password")
        if not password:
            raise ParseError("Please fill password field.")
        if len(password) < 6 or sum(1 for c in password if c.isupper()) < 2 or not re.search(r'\W', password):
            raise ParseError(
                "Password should include at least one captal alphabet and one symbol(ex:!,@,#,etc).")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.password =password => saving raw password. Never do.
            user.set_password(password)  # => hash by django
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    def get(self, request, username):
        user = models.User.objects.get(username=username)
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class HostRoom(APIView):
    def get(self, request, username):
        rooms = Room.objects.filter(owner__username=username)
        serializer = RoomListSerializer(
            rooms, many=True, context={"request": request})
        return Response(serializer.data)


# User가쓴 review check. 나중에 user에게 쓴 review도 하기
class UserReview(APIView):
    def get(self, request, username):
        reviews = Review.objects.filter(user__username=username)
        serializer = ReviewSerializer(
            reviews, many=True)
        return Response(serializer.data)


# class HostReview(APIView):
#     def get(self, request, username):
#         reviews = Review.objects.filter(owner__username=username)
#         serializer = HostReviewSerializer(
#             reviews, many=True, context={"request": request})
#         return Response(serializer.data)
