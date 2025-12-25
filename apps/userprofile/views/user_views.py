from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..models import UserProfile
from ..serializers import UserRead,UserUpdate


class UserProfileViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    http_method_names=["get","patch"]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action=="partial_update":
            return UserUpdate.UserUpdateSerializer
        
        return UserRead.UserReadSerializer



