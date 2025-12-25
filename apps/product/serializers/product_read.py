from rest_framework import serializers
from ..models import Product

class ProductReadSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=["id","sku","name","description","stock_quantity"]
        
        