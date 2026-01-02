from rest_framework import serializers
from ..models import UserProfile

class AdminUpdateSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=False)

    class Meta:
        model=UserProfile
        fields=["first_name","last_name","username","password","email","profile_picture","role"]