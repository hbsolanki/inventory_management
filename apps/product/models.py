from django.db import models
from ..organization.models import Organization
from ..userprofile.models import UserProfile

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=200,blank=True)
    sku=models.CharField(max_length=100)
    stock_quantity=models.IntegerField(default=0)
    organization=models.ForeignKey(to=Organization,on_delete=models.CASCADE,related_name="products")
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(to=UserProfile,on_delete=models.SET_NULL,related_name="product_created",null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(to=UserProfile,on_delete=models.SET_NULL,related_name="product_updated",null=True,blank=True)


    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table="inventory_product"
        indexes=[models.Index(fields=['organization','-created_at'])]
        constraints=[models.UniqueConstraint(fields=["organization","sku"],name="unique_sku_per_organization")]

