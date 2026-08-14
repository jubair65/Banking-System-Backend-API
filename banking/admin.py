from django.contrib import admin

from .models import BankAccount


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