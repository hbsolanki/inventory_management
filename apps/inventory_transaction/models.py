from django.db import models
from ..organization.models import Organization
from ..product.models import Product
from ..userprofile.models import UserProfile


class InventoryTransaction(models.Model):
    action_types=[
        ("IN","Stock In"),
        ("OUT","Stock Out")
    ]

    action=models.CharField(max_length=10,choices=action_types)
    description=models.CharField(max_length=200)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="inventory_transactions")
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(to=UserProfile,on_delete=models.SET_NULL,related_name="inventory_created",null=True,blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(to=UserProfile,on_delete=models.SET_NULL,related_name="inventory_updated",null=True,blank=True)



    class Meta:
        db_table="inventory_transaction"
        indexes=[models.Index(fields=["-created_at"])]


class InventoryTransactionItem(models.Model):
    transaction=models.ForeignKey(InventoryTransaction,on_delete=models.CASCADE,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField()

    class Meta:
        db_table="inventory_transaction_item"