from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rooms import views as room_views

# django는 순서가 중요!
# path("@<str:username>", views.PublicUser.as_view()), @를 사용하면 username validation이 필요없이 myprofile 를 사용가능.
# 지금은 'myprofile'를 사용 못하도록 validate 함
urlpatterns = [
    path("", views.Users.as_view()),
    path("my-profile", views.MyProfile.as_view()),
    path("my-profile/change-password", views.ChangePassword.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogIn.as_view()),
    path("github", views.GithubLogIn.as_view()),
    path("kakao", views.KakaoLogIn.as_view()),
    path("user-profile/<str:username>", views.PublicUser.as_view()),
    path("user-profile/<str:username>/rooms", views.HostRoom.as_view()),
    path("user-profile/<str:username>/reviewsbyuser", views.UserReview.as_view()),
    # path("user-profile/<str:username>/reviewsforuser", views.HostReview.as_view()),
]
