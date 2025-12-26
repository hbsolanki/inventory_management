from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InventoryTransaction
from .serializers import Inventory_transaction_create,Inventory_transaction_read


class InventoryTransViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Inventory_transaction_read.InventoryTransReadSerializer

    def get_queryset(self):
        return InventoryTransaction.objects.filter(user=self.request.user).prefetch_related("items__product").order_by("-created_at")
    
    def get_serializer_class(self):
        if self.action=="create":
            return Inventory_transaction_create.InventoryTransCreateSerializer
        
        return Inventory_transaction_read.InventoryTransReadSerializer
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data,context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()

        return Response({"message":"Transaction Complate"}) 