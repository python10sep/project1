"""
Serializers for Portal API
"""

from rest_framework import serializers
from core.models import Portal


class PortalSerializer(serializers.ModelSerializer):
    """Serializer class for Portal list view"""

    class Meta:
        model = Portal
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PortalDetailSerializer(PortalSerializer):
    """Serializer class for Portal detail view"""

    class Meta(PortalSerializer.Meta):
        fields = PortalSerializer.Meta.fields + ["description"]
