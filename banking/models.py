import random

from django.conf import settings
from django.db import models


def generate_account_number():
    while True:
        account_number = str(random.randint(1000000000, 9999999999))

        if not BankAccount.objects.filter(
            account_number=account_number
        ).exists():
            return account_number


class BankAccount(models.Model):
    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        BLOCKED = "blocked", "Blocked"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_account",
    )
    account_number = models.CharField(
        max_length=10,
        unique=True,
        editable=False,
    )
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"