from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InventoryTransaction
from .serializers import Inventory_transaction_create,Inventory_transaction_read
from django.core.cache import cache
from .services.inventory_services import create_inventory_transaction,delete_cache_inventory
from apps.permission.organization import IsManagerOrAdmin


class InventoryTransViewSet(ModelViewSet):

    def get_queryset(self):
        return InventoryTransaction.objects.filter(organization=self.request.user.organization).prefetch_related("items__product").order_by("-created_at")
       
    
    def get_serializer_class(self):
        if self.action=="create":
            return Inventory_transaction_create.InventoryTransCreateSerializer
        
        return Inventory_transaction_read.InventoryTransReadSerializer
    
    def get_permissions(self,) :
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsManagerOrAdmin()]
        
        return [IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        cache_key=f"inventory:{self.request.user.organization.id}"
        data=cache.get(cache_key)
        if data :
            return Response(data)
        
        products_data=self.get_queryset()
        serializer=Inventory_transaction_read.InventoryTransReadSerializer(products_data,many=True)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)

    def perform_create(self, serializer):
        create_inventory_transaction(
            organization=self.request.user.organization,
            action=serializer.validated_data["action"],
            description=serializer.validated_data["description"],
            items=serializer.validated_data["items"],
            user=self.request.user
        )
        delete_cache_inventory(organization=self.request.user.organization)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
        delete_cache_inventory(organization=self.request.user.organization)

    def perform_destroy(self, instance):
        instance.delete()
        delete_cache_inventory(organization=self.request.user.organization)