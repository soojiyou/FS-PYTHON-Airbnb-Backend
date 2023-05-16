from django.urls import path
from . import views

urlpatterns = [
    path("room-category", views.CategoryRoomViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path("room-category/<int:pk>", views.CategoryRoomViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    })),
    path("experience-category", views.CategoryExperienceViewSet.as_view({
         'get': 'list',
         'post': 'create',
         })),
    path("experience-category/<int:pk>", views.CategoryExperienceViewSet.as_view({
        'get': 'retrieve',
        'put': 'partial_update',
        'delete': 'destroy',
    })),
]
