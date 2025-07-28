from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reactor
from .serializers import ReactorSerializer, ReactorProjectionSerializer

class ReactorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving reactors
    """
    