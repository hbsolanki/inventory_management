from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import product_create,product_stock_update,product_read,product_update
from .models import Product


class ProductViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action =="update_stock":
            return product_stock_update.ProductStockSerializer
        elif self.action == "create":
            return product_create.ProductCreateSerializer
        elif self.action=="partial_update":
            return product_update.ProductUpdateSerializer
        
        return product_read.ProductReadSerializer
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

    @action(detail=True,methods=["PATCH"])
    def update_stock(self,request,pk=None):
        product=self.get_object()

        serializer=product_stock_update.ProductStockSerializer(data=request.data,context={"product":product,"user":request.user})
        serializer.is_valid(raise_exception=True)
        quantity=serializer.validated_data.get("quantity")
        action=serializer.validated_data.get("action")

        if(action=="IN"):
            product.stock_quantity+=quantity
        else:
            product.stock_quantity-=quantity

        product.save(update_fields=["stock_quantity"])

        return Response({"message":"stock update successfuly","current_stock":product.stock_quantity})
        