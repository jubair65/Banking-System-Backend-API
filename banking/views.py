from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import BankAccount
from .serializers import BankAccountSerializer


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