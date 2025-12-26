from rest_framework import serializers
from django.db import transaction
from ..models import InventoryTransaction,InventoryTransactionItem
from ...product.models import Product

class InventoryTransItemSerializer(serializers.Serializer):
    productId=serializers.IntegerField(required=True)
    quantity=serializers.IntegerField(required=True)

class InventoryTransCreateSerializer(serializers.Serializer):
    action=serializers.ChoiceField(choices=["IN","OUT"])
    description=serializers.CharField(required=False)
    items=InventoryTransItemSerializer(many=True)

    def validate_item(self,items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        
        return items



    def create(self, validated_data):
        user=self.context.get("user")
        items=validated_data.get("items")
        action=validated_data.get("action")
        description=validated_data.get("description","")

        try:
            with transaction.atomic():
                curr_transaction=InventoryTransaction.objects.create(
                    user=user,
                    action=action,
                    description=description      
                )

                for item in items:
                    if item.get("productId") and item.get("quantity"):
                        quantity=item.get("quantity")
                        productId=item.get("productId")
                        product=Product.objects.get(id=productId)
                        if product:
                            if action=="OUT" and quantity>product.stock_quantity:
                                raise serializers.ValidationError({"quantity":f"Insufficient stock for product id-{productId} sku-{product.sku}"})
        
                            if action=="OUT":
                                product.stock_quantity-=quantity
                            else:
                                product.stock_quantity+=quantity

                            product.save(update_fields=["stock_quantity"])

                            InventoryTransactionItem.objects.create(transaction=curr_transaction,product=product,quantity=quantity)

        except Exception as e:
            raise serializers.ValidationError(e)


        return curr_transaction
            

        

