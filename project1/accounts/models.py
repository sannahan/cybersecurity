from django.db import models

from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField

class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    iban = models.CharField(max_length=34, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    balance = models.BigIntegerField(default=0)

class Card(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # card_number = EncryptedCharField(max_length=16, unique=True)
    card_number = models.CharField(max_length=16, unique=True)

