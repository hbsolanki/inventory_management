from rest_framework import serializers
from ..models import Product


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=["id","sku","name","description"]
        

    def validate_sku(self, value):
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("SKU already Exist!!")
        
        return value