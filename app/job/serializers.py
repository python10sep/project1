"""
Serializers for Job API
"""

from rest_framework import serializers
from core.models import JobTitle, Portal, JobDescription


class JobTitleSerializer(serializers.ModelSerializer):
    """Serializer for job titles"""

    class Meta:
        model = JobTitle
        fields = ["id", "title"]
        read_only_fields = ["id"]


class PortalSerializer(serializers.ModelSerializer):
    """Serializer for Portal"""

    class Meta:
        Model = Portal
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class JobDescriptionSerializer(serializers.ModelSerializer):
    """Serializer for JobDescription"""

    class Meta:
        Model = JobDescription
        fields = ["id", "role", "description_text", "pub_date"]
        read_only_fields = ["id"]


