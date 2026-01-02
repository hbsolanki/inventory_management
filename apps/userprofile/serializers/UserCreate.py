from rest_framework import serializers
from ..models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=UserProfile
        fields=["first_name","last_name","username","password","email"]
