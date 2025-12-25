from rest_framework import serializers
from ..models import Product


class ProductStockSerializer(serializers.Serializer):
    quantity=serializers.IntegerField(min_value=1)
    action=serializers.ChoiceField(choices=["IN","OUT"])
    
    def validate(self, attrs):
        product=self.context["product"]
        quantity=attrs["quantity"]
        action=attrs["action"]

        if action=="OUT" and quantity>product.stock_quantity:
            raise serializers.ValidationError({"quantity":"Insufficient stock"})
        
        return attrs
        