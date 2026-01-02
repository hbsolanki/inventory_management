from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .serializers import product_create,product_read,product_update
from .models import Product
from .services.product_service import delete_cache_inventory
from apps.permission.organization import IsAdmin,IsManagerOrAdmin,IsManager,IsEmployee
import datetime


class ProductViewSet(ModelViewSet):

    def get_queryset(self):
        return Product.objects.filter(organization=self.request.user.organization)
    
    def get_serializer_class(self):
        if self.action == "create":
            return product_create.ProductCreateSerializer
        elif self.action=="partial_update":
            return product_update.ProductUpdateSerializer
        
        return product_read.ProductReadSerializer
    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        cache_key=f"product:list:{self.request.user.organization}"
        data=cache.get(cache_key)
        if data :
            return Response(data)
        
        products_data=self.get_queryset()
        serializer=product_read.ProductReadSerializer(products_data,many=True)
       
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        productId=kwargs.get("pk")
        cache_key=f"product:{self.request.user.organization}:{productId}"
        data=cache.get(cache_key)
        if data:
            return Response(data)
        
        dataset=self.get_object()
        serializer=self.get_serializer(dataset)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        product = serializer.save(updated_by=self.request.user)
        delete_cache_inventory(organizationId=product.organization,productId=product.id)
        
    def perform_destroy(self, instance):
        delete_cache_inventory(organizationId=instance.organization,productId=instance.id)
        instance.delete()
    
    def perform_create(self, serializer):
        product = serializer.save(organization=self.request.user.organization,created_by=self.request.user)
        delete_cache_inventory(organizationId=product.organization)
