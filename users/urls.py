from django.urls import path
from . import views
from rooms import views as room_views

# django는 순서가 중요!
# path("@<str:username>", views.PublicUser.as_view()), @를 사용하면 username validation이 필요없이 myprofile 를 사용가능.
# 지금은 'myprofile'를 사용 못하도록 validate 함
urlpatterns = [
    path("", views.Users.as_view()),
    path("myprofile", views.MyProfile.as_view()),
    path("myprofile/change-password", views.ChangePassword.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/rooms", views.HostRoom.as_view()),
    path("@<str:username>/reviewsbyuser", views.UserReview.as_view()),
    # path("<str:username>/reviewsforuser", views.HostReview.as_view()),
]
