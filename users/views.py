import re
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from . import serializers


class Me(APIView):

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
        if username == "me":
            raise ("'me' cannot be used for username!")
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
        pass
