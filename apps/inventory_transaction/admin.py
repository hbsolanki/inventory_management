from django.contrib import admin
from .models import InventoryTransaction,InventoryTransactionItem


admin.site.register(InventoryTransaction)
admin.site.register(InventoryTransactionItem)