from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InventoryTransaction
from .serializers import Inventory_transaction_create,Inventory_transaction_read
from django.core.cache import cache


class InventoryTransViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Inventory_transaction_read.InventoryTransReadSerializer

    def get_queryset(self):
        return InventoryTransaction.objects.filter(user=self.request.user).prefetch_related("items__product").order_by("-created_at")
       
    
    def get_serializer_class(self):
        if self.action=="create":
            return Inventory_transaction_create.InventoryTransCreateSerializer
        
        return Inventory_transaction_read.InventoryTransReadSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key=f"inventory:{self.request.user.id}"
        data=cache.get(cache_key)
        if data :
            return Response(data)
        
        products_data=self.get_queryset()
        serializer=Inventory_transaction_read.InventoryTransReadSerializer(products_data,many=True)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data,context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache_key=f"inventory:{self.request.user.id}"
        cache.delete(cache_key)

        return Response({"message":"Transaction Complate"}) 
    
    def perform_update(self, serializer):
        serializer.save()
        cache_key=f"inventory:{self.request.user.id}"
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        instance.delete()
        cache_key=f"inventory:{self.request.user.id}"
        cache.delete(cache_key)