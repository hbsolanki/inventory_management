from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.userprofile.models import UserProfile
from apps.userprofile.serializers import UserRead,UserUpdate
from django.core.cache import cache


class UserProfileViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    http_method_names=["get","patch"]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action=="partial_update":
            return UserUpdate.UserUpdateSerializer
        
        return UserRead.UserReadSerializer

    def retrieve(self, request, *args, **kwargs):
        cache_key=f"user:{self.request.user.id}"
        data=cache.get(cache_key)
        if data:
            return Response(data)
        
        dataset=self.get_object()
        serializer=self.get_serializer(dataset)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)
    