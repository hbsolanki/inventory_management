from rest_framework import serializers
from ..models import InventoryTransaction,InventoryTransactionItem

class InventoryTransItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=InventoryTransactionItem
        fields=["id","product","quantity"]

class InventoryTransReadSerializer(serializers.ModelSerializer):
    items=InventoryTransItemSerializer(many=True,read_only=True)
    class Meta:
        model=InventoryTransaction
        fields=["id","action","description","created_at","items"]
    


