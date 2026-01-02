from rest_framework import serializers
from apps.userprofile.models import UserProfile
from apps.userprofile.serializers.UserCreate import UserProfileCreateSerializer


class OrganizationCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=70)
    description = serializers.CharField(max_length=200, allow_blank=True)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email=serializers.EmailField()

    def validate_username(self, value):
        if UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
