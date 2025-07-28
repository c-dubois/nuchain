from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reactor
from .serializers import ReactorSerializer, ReactorProjectionSerializer

class ReactorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving reactors
    Only provides basic reactor info for investment decisions
    """
    queryset = Reactor.objects.filter(is_active=True)
    serializer_class = ReactorSerializer
    permission_classes = [IsAuthenticated]