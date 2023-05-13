import re
import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
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
        if username == "my-profile" or "user-profile":
            raise ("'my-profile' or 'user-profile' cannot be used for username!")
        password = request.data.get("password")
        if not password:
            raise ParseError("Please fill password field.")
        if len(password) < 6 or sum(1 for c in password if c.isupper()) < 2 or not re.search(r'\W', password):
            raise ParseError(
                "Password should be included at least one captal alphabet and one symbol(ex:!,@,#,etc).")
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
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound
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


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise ParseError(
                "Please fill both old password and new password field.")
        if user.check_password(old_password):
            if len(new_password) < 6 or sum(1 for c in new_password if c.isupper()) < 1 or not re.search(r'\W', new_password):
                raise ParseError(
                    "new password should include at least one captal alphabet and one symbol(ex:!,@,#,etc).")
            user.set_password(new_password)  # this only hash password
            user.save()
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username and password:
            raise ParseError("Please provide both username and password.")
        user = authenticate(request, username=username, password=password,)
        if user:
            # django let user to login by creating session on the backend, and give cookie to user
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Wrong Password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})


# JWT login view
class JWTLogIn(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})

# github login


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=d049c38387c8383af63e&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"})
            access_token = access_token.json().get('access_token')
            user_data = requests.get("https://api.github.com/user",
                                     headers={
                                         "Authorization": f"Bearer {access_token}",
                                         "Accept": "application/json",
                                     },
                                     )
            user_data = user_data.json()
            user_emails = requests.get("https://api.github.com/user/emails",
                                       headers={
                                           "Authorization": f"Bearer {access_token}",
                                           "Accept": "application/json",
                                       },
                                       )
            user_emails = user_emails.json()
            try:
                user = models.User.objects.get(email=user_emails[0]['email'])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    username=user_data.get('login'),
                    email=user_emails[0]['email'],
                    name=user_data.get('name'),
                    avatar=user_data.get('avatar_url'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_308_PERMANENT_REDIRECT)
