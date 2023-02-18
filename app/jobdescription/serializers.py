"""
Serializers for JobDescription API
"""

from rest_framework import serializers
from core.models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    """Serializer class for JobDescription list view"""

    class Meta:
        model = JobDescription
        fields = ["id", "role"]
        read_only_fields = ["id"]


class JobDescriptionDetailSerializer(JobDescriptionSerializer):
    """Serializer class for JobDescription detail view"""

    class Meta(JobDescriptionSerializer.Meta):
        fields = JobDescriptionSerializer.Meta.fields + [
            "description_text", "pub_date"
        ]
