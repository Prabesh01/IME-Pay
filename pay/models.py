from django.db import models

class Transaction(models.Model):
  TranAmount = models.DecimalField(max_digits=6, decimal_places=2)
  RefId = models.CharField(unique=True, max_length = 20)
  TokenId = models.CharField(max_length = 20)
  TransactionId = models.CharField(max_length = 20)
  Msisdn = models.CharField(max_length = 20)
  ImeTxnStatus = models.SmallIntegerField(null=True, blank=True)
  RequestDate = models.DateTimeField(blank=True)
  ResponseDate = models.DateTimeField(null=True, blank=True)