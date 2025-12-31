from django.core.cache import cache

def delete_cache_inventory(*,userId,productId=None):
    cache.delete(f"product:list:{userId}")
    if productId:
        cache.delete(f"product:{userId}:{productId}")