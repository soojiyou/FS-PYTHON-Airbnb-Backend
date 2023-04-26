from django.urls import path
from . import views

# django는 순서가 중요!
urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("<str:username>", views.PublicUser.as_view()),
]
