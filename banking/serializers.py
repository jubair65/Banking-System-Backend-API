from rest_framework import serializers

from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    account_holder = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = (
            "id",
            "account_number",
            "account_holder",
            "account_type",
            "balance",
            "status",
            "created_at",
        )
        read_only_fields = (
            "id",
            "account_number",
            "account_holder",
            "balance",
            "status",
            "created_at",
        )

    def get_account_holder(self, obj):
        return obj.user.get_full_name() or obj.user.username