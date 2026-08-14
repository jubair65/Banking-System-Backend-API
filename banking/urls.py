from django.urls import path

from .views import (
    CreateBankAccountView,
    MyBankAccountView,
    DepositView,
    WithdrawView,
    TransferView,
)

urlpatterns = [
    path("account/create/",CreateBankAccountView.as_view(),name="account-create",),
    path("account/me/",MyBankAccountView.as_view(),name="account-me",),
    path("deposit/",DepositView.as_view(),name="deposit",),
    path("withdraw/",WithdrawView.as_view(),name="withdraw",),
    path("transfer/",TransferView.as_view(),name="transfer",),
]