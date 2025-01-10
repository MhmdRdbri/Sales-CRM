from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Factors
from .serializers import FactorSerializer


class FactorListCreateView(generics.ListCreateAPIView):
    queryset = Factors.objects.prefetch_related('items').all()
    serializer_class = FactorSerializer
    permission_classes = [IsAuthenticated]
