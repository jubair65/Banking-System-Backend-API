from django.urls import path

from .views import (
    CreateBankAccountView,
    MyBankAccountView,
    DepositView,
    WithdrawView,
    TransferView,
    TransactionHistoryView,
    AdminAccountListView,
    AdminAccountDetailView,
    AdminTransactionListView,
    AdminAccountTransactionListView,
)

urlpatterns = [
    path("account/create/",CreateBankAccountView.as_view(),name="account-create",),
    path("account/me/",MyBankAccountView.as_view(),name="account-me",),
    path("deposit/",DepositView.as_view(),name="deposit",),
    path("withdraw/",WithdrawView.as_view(),name="withdraw",),
    path("transfer/",TransferView.as_view(),name="transfer",),
    path("transactions/",TransactionHistoryView.as_view(),name="transactions",),
    path("admin/accounts/",AdminAccountListView.as_view(),name="admin-accounts",),
    path("admin/accounts/<int:pk>/",AdminAccountDetailView.as_view(),name="admin-account-detail",),
    path("admin/transactions/",AdminTransactionListView.as_view(),name="admin-transactions",),
    path("admin/transactions/<int:account_id>/",AdminAccountTransactionListView.as_view(),name="admin-account-transactions",),
]