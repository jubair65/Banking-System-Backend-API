from django.urls import path

from .views import (
    CreateBankAccountView,
    MyBankAccountView,
)

urlpatterns = [
    path("account/create/",CreateBankAccountView.as_view(),name="account-create",),
    path("account/me/",MyBankAccountView.as_view(),name="account-me",),
]