import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied


class PhotoDetail(APIView):

    # protecting
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (photo.experience and photo.experience.host != request.user):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURL(APIView):
    def post(self, request):
        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
        temp_post_url = requests.post(url, headers={
            "Authorization": f"Bearer {settings.CF_TOKEN}",
        })
        temp_post_url = temp_post_url.json()
        result = temp_post_url.get('result')
        return Response({"id": result.get("id"), 'uploadURL': result.get('uploadURL')})
