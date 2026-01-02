from rest_framework import serializers

class InventoryTransItemSerializer(serializers.Serializer):
    productId=serializers.IntegerField(required=True)
    quantity=serializers.IntegerField(required=True)

class InventoryTransCreateSerializer(serializers.Serializer):
    action=serializers.ChoiceField(choices=["IN","OUT"])
    description=serializers.CharField(required=True)
    items=InventoryTransItemSerializer(many=True)

    def validate_item(self,items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        
        return items

