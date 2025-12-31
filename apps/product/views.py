from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import product_create,product_read,product_update
from .models import Product
from django.core.cache import cache
from .services.product_service import delete_cache_inventory


class ProductViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == "create":
            return product_create.ProductCreateSerializer
        elif self.action=="partial_update":
            return product_update.ProductUpdateSerializer
        
        return product_read.ProductReadSerializer
    
    def list(self, request, *args, **kwargs):
        cache_key=f"product:list:{self.request.user.id}"
        data=cache.get(cache_key)
        if data :
            return Response(data)
        
        products_data=self.get_queryset()
        serializer=product_read.ProductReadSerializer(products_data,many=True)
       
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        productId=kwargs.get("pk")
        cache_key=f"product:{self.request.user.id}:{productId}"
        data=cache.get(cache_key)
        if data:
            return Response(data)
        
        dataset=self.get_object()
        serializer=self.get_serializer(dataset)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        product = serializer.save()
        delete_cache_inventory(userId=product.user.id,productId=product.id)
        
    def perform_destroy(self, instance):
        delete_cache_inventory(userId=instance.user.id,productId=instance.id)
        instance.delete()
    
    def perform_create(self, serializer):
        product = serializer.save(user=self.request.user)
        delete_cache_inventory(userId=product.user.id)
