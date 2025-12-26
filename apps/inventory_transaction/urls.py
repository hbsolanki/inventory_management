from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import InventoryTransViewSet

router=DefaultRouter()
router.register("",InventoryTransViewSet,basename="inventry_transaction")

urlpatterns = [
    path('',include(router.urls))
]
