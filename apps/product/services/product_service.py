from django.core.cache import cache

def delete_cache_inventory(*,organizationId,productId=None):
    cache.delete(f"product:list:{organizationId}")
    if productId:
        cache.delete(f"product:{organizationId}:{productId}")