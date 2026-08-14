from django.urls import path

from .views import (
    SignupView,
    LoginView,
    ProfileView,
    AdminUserListView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("admin/users/",AdminUserListView.as_view(),name="admin-users",),
]