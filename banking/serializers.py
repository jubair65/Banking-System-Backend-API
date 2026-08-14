from rest_framework import serializers
from .models import BankAccount,Transaction
from decimal import Decimal


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







class MoneyTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )


class TransactionSerializer(serializers.ModelSerializer):
    from_account_number = serializers.SerializerMethodField()
    to_account_number = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "type",
            "amount",
            "from_account_number",
            "to_account_number",
            "timestamp",
        )

    def get_from_account_number(self, obj):
        if obj.from_account:
            return obj.from_account.account_number
        return None

    def get_to_account_number(self, obj):
        if obj.to_account:
            return obj.to_account.account_number
        return None


class TransferSerializer(serializers.Serializer):
    to_account = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
