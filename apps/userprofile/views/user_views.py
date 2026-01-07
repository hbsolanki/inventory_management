from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..serializers import UserCreate,UserRead,UserUpdate,AdminUpdate
from rest_framework.decorators import action
from ..services.user_service import create_user
from ..models import UserProfile
from ...permission.organization import IsAdmin,IsManagerOrAdmin,CanModifyUser,CanDeleteUser
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache


class UserProfileViewSet(ModelViewSet):
    
    def get_serializer_class(self):
        if self.action=='create_manager':
            return UserCreate.UserProfileCreateSerializer
        elif self.action=='create_employee':
            return UserCreate.UserProfileCreateSerializer
        elif self.action=='partial_update':
            if self.request.user.role==UserProfile.ROLE_ADMIN:
                return AdminUpdate.AdminUpdateSerializer
            return UserUpdate.UserUpdateSerializer
    
        return UserRead.UserReadSerializer
    
    def get_permissions(self) :
        if self.action in ["update", "partial_update"]:
            return [CanModifyUser()]
        if self.action in ["destroy","delete"]:
            return [CanDeleteUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user=self.request.user
        if user.role==UserProfile.ROLE_ADMIN:
            return UserProfile.objects.filter(organization=user.organization)
        if user.role==UserProfile.ROLE_MANAGER:
            return UserProfile.objects.filter(organization=user.organization,role=UserProfile.ROLE_EMPLOYEE)
        print(user.id)
        return UserProfile.objects.filter(id=user.id)
    
    @action(detail=False,methods=["POST"],url_path="create/manager",permission_classes=[IsAdmin])
    def create_manager(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=create_user(
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            username=serializer.validated_data["username"],
            organization=request.user.organization,
            password=serializer.validated_data["password"],
            email=serializer.validated_data["email"],
            role=UserProfile.ROLE_MANAGER
        )

        return Response({"message":"manager created","manager":{"id":user.id,"username":user.username}},status=status.HTTP_201_CREATED)

    @action(detail=False,methods=["POST"],url_path="create/employee",permission_classes=[IsManagerOrAdmin])
    def create_employee(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=create_user(
             first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            username=serializer.validated_data["username"],
            organization=request.user.organization,
            password=serializer.validated_data["password"],
            email=serializer.validated_data["email"],
            role=UserProfile.ROLE_EMPLOYEE
        )

        return Response({"message":"employee created","employee":{"id":user.id,"username":user.username}},status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        cache_key=f"user:{kwargs['pk']}"
        data=cache.get(cache_key)
        if data:
            return Response(data)
        
        dataset=self.get_object()
        serializer=self.get_serializer(dataset)
        cache.set(cache_key,serializer.data,timeout=180)
        return Response(serializer.data)
    
    @action(detail=False,methods=["GET"],url_path="manager",permission_classes=[IsAdmin])
    def manager_list(self,request):
        manager=UserProfile.objects.filter(organization=request.user.organization,role=UserProfile.ROLE_MANAGER)
        serializer=UserRead.UserReadSerializer(manager,many=True)

        return Response(serializer.data)

    @action(detail=False,methods=["GET"],url_path="employee",permission_classes=[IsManagerOrAdmin])
    def employee_list(self,request):
        employees=UserProfile.objects.filter(organization=request.user.organization,role=UserProfile.ROLE_EMPLOYEE)
        serializer=UserRead.UserReadSerializer(employees,many=True)

        return Response(serializer.data)
    
    def perform_create(self, serializer) :
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer) :
        serializer.save(updated_by=self.request.user)
