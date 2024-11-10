from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]
