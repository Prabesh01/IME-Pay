from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
  list_display = ("RefId", "TranAmount", "ImeTxnStatus","RequestDate")

admin.site.register(Transaction,TransactionAdmin)
