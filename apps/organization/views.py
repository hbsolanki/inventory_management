from collections.abc import Sequence
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  AllowAny,IsAuthenticated
from apps.userprofile.services.user_service import get_tokens_for_user,create_user
from apps.userprofile.models import UserProfile
from .serializer import read,create
from .services.organization_service import create_organization
from .models import Organization


class OrganizationViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action=="create":
            return create.OrganizationCreateSerializer
        
        return read.OrganizationReadSerializer
    
    def get_queryset(self):
        return Organization.objects.filter(id=self.request.user.organization.id)
    
    def get_permissions(self) :
        if self.action=="create":
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization=create_organization(name=serializer.validated_data["name"],description=serializer.validated_data["description"])
        admin_user=create_user(
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            email=serializer.validated_data["email"],
            role=UserProfile.ROLE_ADMIN,
            organization=organization
            )
        
        token=get_tokens_for_user(admin_user)
        return Response( {
                "organization_id": organization.id,
                "admin_username": admin_user.username,
                **token
            },
            status=status.HTTP_201_CREATED,
       )        
