from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets

from rbac.models import Role, Relationship

from rbac.serializers import RoleSerializer, RelationshipSerializer, ContentTypeSerializer


# API views

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Roles to be viewed or edited.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RelationshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Relationships to be viewed or edited.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

	
class ContentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ContentTypes to be viewed or edited.
    """
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
