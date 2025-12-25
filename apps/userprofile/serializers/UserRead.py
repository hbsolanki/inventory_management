from rest_framework import serializers
from ..models import UserProfile


class UserReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=UserProfile
        fields=["id","first_name","last_name","username","profile_picture","email"]
