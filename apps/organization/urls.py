from django.urls import path,include
from .views import OrganizationViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register('',OrganizationViewSet,basename='organization')

urlpatterns = [
    path('',include(router.urls))
]
