from django.urls import path
from .views import PhotoDetail, GetUploadURL

urlpatterns = [
    path("photos/get-upload-url", GetUploadURL.as_view(),),
    path("photos/<int:pk>", PhotoDetail.as_view(),)
]
