from django.db import transaction
from rest_framework.exceptions import ValidationError
from ..models import InventoryTransaction,InventoryTransactionItem
from ...product.models import Product
from django.core.cache import cache


@transaction.atomic
def create_inventory_transaction(*,organization,action,description,items,user):
    curr_transaction=InventoryTransaction.objects.create(
        organization=organization,
        action=action,
        description=description,
        created_by=user,
    )

    products=Product.objects.select_for_update().filter(id__in=[item["productId"] for item in items],organization=organization)

    Product_dict={product.id:product for product in products}

    for item in items:
        product_id=item["productId"]
        product=Product_dict.get(product_id)
        quantity=item["quantity"]

        if not product:
            raise ValidationError(f"Product id {product_id} not found")
        if action=="OUT" and quantity>product.stock_quantity:
            raise ValidationError({"items": [{"productId": product_id,"quantity": f"Insufficient stock for sku {product.sku}"}]})

        if action=="OUT":
            product.stock_quantity-=quantity
        else:
            product.stock_quantity+=quantity

        product.save(update_fields=["stock_quantity"])

        InventoryTransactionItem.objects.create(transaction=curr_transaction,product=product,quantity=quantity)
        cache.delete(f"product:{organization.id}:{product.id}")

        delete_cache_inventory(organization=organization)
    return curr_transaction


def delete_cache_inventory(*,organization):
    cache.delete(f"product:list:{organization}")


