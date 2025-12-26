from rest_framework import serializers
from ..models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=UserProfile
        fields=["first_name","last_name","username","password","email","profile_picture"]

    def create(self, validated_data):
        password=validated_data.get("password")
        user=UserProfile(**validated_data)
        user.set_password(password)
        user.save()

        return user
    