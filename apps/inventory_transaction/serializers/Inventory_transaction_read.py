from rest_framework import serializers
from ..models import InventoryTransaction,InventoryTransactionItem
from ...product.serializers.product_read import ProductReadSerializer

class InventoryTransItemSerializer(serializers.ModelSerializer):
    product=ProductReadSerializer(read_only=True)
    class Meta:
        model=InventoryTransactionItem
        fields=["id","product","quantity"]

class InventoryTransReadSerializer(serializers.ModelSerializer):
    items=InventoryTransItemSerializer(many=True,read_only=True)
    class Meta:
        model=InventoryTransaction
        fields=["id","action","description","created_at","items"]
    


