from rest_framework.serializers import ModelSerializer
from ..models import Organization


class OrganizationReadSerializer(ModelSerializer):

    class Meta:
        model=Organization
        fields=["name","description"]
