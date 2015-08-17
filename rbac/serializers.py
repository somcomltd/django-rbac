from rest_framework import serializers

from .models import Relationship

class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Relationship