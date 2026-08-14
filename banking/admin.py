from django.contrib import admin

from .models import BankAccount,Transaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number",
        "user",
        "account_type",
        "balance",
        "status",
        "created_at",
    )
    list_filter = (
        "account_type",
        "status",
    )
    search_fields = (
        "account_number",
        "user__username",
        "user__email",
    )





@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "from_account",
        "to_account",
        "amount",
        "timestamp",
    )
    list_filter = (
        "type",
        "timestamp",
    )
    search_fields = (
        "from_account__account_number",
        "to_account__account_number",
    )
    ordering = ("-timestamp",)