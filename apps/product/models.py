from django.db import models
from ..userprofile.models import UserProfile

class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=200,blank=True)
    sku=models.CharField(max_length=100,unique=True)
    stock_quantity=models.IntegerField(default=0)
    user=models.ForeignKey(to=UserProfile,on_delete=models.CASCADE,related_name="products")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table="inventory_product"
        indexes=[models.Index(fields=['user','-created_at'])]
        constraints=[models.UniqueConstraint(fields=["user","sku"],name="unique_sku_per_user")]

