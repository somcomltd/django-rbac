from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Role, Relationship

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Relationship


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType