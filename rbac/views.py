from django.shortcuts import render

from rest_framework import viewsets

from rbac.models import Relationship

from rbac.serializers import RelationshipSerializer


# API views

class RelationshipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows subscriptions to be viewed or edited.
    """
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
