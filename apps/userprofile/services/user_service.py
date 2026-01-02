from rest_framework_simplejwt.tokens import RefreshToken
from ..models import UserProfile

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

def create_user(*,first_name,last_name,email,username,organization,role,password):
    user=UserProfile.objects.create_user(
        first_name=first_name,last_name=last_name,email=email,username=username,organization=organization,password=password,role=role
    )

    return user
    