from django.urls import path,include
from .views.auth_views import RegisterView,LoginView
from .views.user_views import UserProfileViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('',UserProfileViewSet,basename='user')

urlpatterns = [
    path('register/',RegisterView.as_view(),name='user_register'),
    path('login/',LoginView.as_view(),name='user_login'),
    path('',include(router.urls))
]
