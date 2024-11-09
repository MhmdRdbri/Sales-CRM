# views.py
from rest_framework import viewsets
from .models import SalesOpportunity
from .serializers import SalesOpportunitySerializer
from rest_framework.permissions import IsAuthenticated


class SalesOpportunityViewSet(viewsets.ModelViewSet):
    queryset = SalesOpportunity.objects.all()
    serializer_class = SalesOpportunitySerializer
    permission_classes = [IsAuthenticated]
