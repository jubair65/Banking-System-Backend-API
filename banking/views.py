from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import BankAccount,Transaction
from .serializers import BankAccountSerializer,TransferSerializer
from rest_framework import status
from rest_framework.response import Response
from .serializers import MoneyTransactionSerializer
from django.db import transaction as db_transaction


class CreateBankAccountView(generics.CreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, "bank_account"):
            return Response(
                {"detail": "You already have a bank account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyBankAccountView(generics.RetrieveAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.bank_account


class DepositView(generics.GenericAPIView):
    serializer_class = MoneyTransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        try:
            account = request.user.bank_account
        except BankAccount.DoesNotExist:
            return Response(
                {"detail": "Bank account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if account.status != BankAccount.Status.ACTIVE:
            return Response(
                {"detail": "Bank account is blocked."},
                status=status.HTTP_403_FORBIDDEN,
            )

        with db_transaction.atomic():
            account = BankAccount.objects.select_for_update().get(
                pk=account.pk
            )

            account.balance += amount
            account.save(update_fields=["balance"])

            Transaction.objects.create(
                from_account=account,
                amount=amount,
                type=Transaction.TransactionType.DEPOSIT,
            )

        return Response(
            {
                "message": "Deposit successful.",
                "account_number": account.account_number,
                "amount": amount,
                "balance": account.balance,
            },
            status=status.HTTP_200_OK,
        )


class WithdrawView(generics.GenericAPIView):
    serializer_class = MoneyTransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]

        try:
            account = request.user.bank_account
        except BankAccount.DoesNotExist:
            return Response(
                {"detail": "Bank account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if account.status != BankAccount.Status.ACTIVE:
            return Response(
                {"detail": "Bank account is blocked."},
                status=status.HTTP_403_FORBIDDEN,
            )

        with db_transaction.atomic():
            account = BankAccount.objects.select_for_update().get(
                pk=account.pk
            )

            if account.balance < amount:
                return Response(
                    {"detail": "Insufficient balance."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            account.balance -= amount
            account.save(update_fields=["balance"])

            Transaction.objects.create(
                from_account=account,
                amount=amount,
                type=Transaction.TransactionType.WITHDRAW,
            )

        return Response(
            {
                "message": "Withdrawal successful.",
                "account_number": account.account_number,
                "amount": amount,
                "balance": account.balance,
            },
            status=status.HTTP_200_OK,
        )



class TransferView(generics.GenericAPIView):
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        receiver_account_number = serializer.validated_data["to_account"]

        try:
            sender = request.user.bank_account
        except BankAccount.DoesNotExist:
            return Response(
                {"detail": "Sender bank account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if sender.status != BankAccount.Status.ACTIVE:
            return Response(
                {"detail": "Sender bank account is blocked."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            receiver = BankAccount.objects.get(
                account_number=receiver_account_number
            )
        except BankAccount.DoesNotExist:
            return Response(
                {"detail": "Receiver bank account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if sender.pk == receiver.pk:
            return Response(
                {"detail": "You cannot transfer money to your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if receiver.status != BankAccount.Status.ACTIVE:
            return Response(
                {"detail": "Receiver bank account is blocked."},
                status=status.HTTP_403_FORBIDDEN,
            )

        with db_transaction.atomic():
            account_ids = sorted([sender.pk, receiver.pk])

            locked_accounts = list(
                BankAccount.objects
                .select_for_update()
                .filter(pk__in=account_ids)
                .order_by("pk")
            )

            locked_accounts_by_id = {
                account.pk: account for account in locked_accounts
            }

            sender = locked_accounts_by_id[sender.pk]
            receiver = locked_accounts_by_id[receiver.pk]

            if sender.balance < amount:
                return Response(
                    {"detail": "Insufficient balance."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            sender.balance -= amount
            receiver.balance += amount

            sender.save(update_fields=["balance"])
            receiver.save(update_fields=["balance"])

            transaction_record = Transaction.objects.create(
                from_account=sender,
                to_account=receiver,
                amount=amount,
                type=Transaction.TransactionType.TRANSFER,
            )

        return Response(
            {
                "message": "Transfer successful.",
                "transaction_id": transaction_record.id,
                "from_account": sender.account_number,
                "to_account": receiver.account_number,
                "amount": amount,
                "sender_balance": sender.balance,
                "receiver_balance": receiver.balance,
            },
            status=status.HTTP_200_OK,
        )

