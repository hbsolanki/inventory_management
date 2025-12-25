from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import authenticate
from ..serializers.UserCreate import UserProfileCreateSerializer
from ..services.auth_service import get_tokens_for_user


class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()

        token=get_tokens_for_user(user)

        return Response({**token,"user":{"id":user.id,"username":user.username}},status=201)


class LoginThrottle(AnonRateThrottle):
    rate='5/min'


class LoginView(APIView):
    permission_classes=[AllowAny]
    throttle_classes=[LoginThrottle]

    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")

        user=authenticate(username=username,password=password)

        if not user : 
            return Response({"error":"Invalid Credentials"},status=401)
        
        token=get_tokens_for_user(user)

        return Response({**token,"user":{"id":user.id,"username":user.username}})
