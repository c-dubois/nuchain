from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reactor
from .serializers import ReactorSerializer

class ReactorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving reactors
    Only provides basic reactor info for investment decisions
    """
    queryset = Reactor.objects.filter(is_active=True).order_by('display_order')
    serializer_class = ReactorSerializer
    permission_classes = [IsAuthenticated]