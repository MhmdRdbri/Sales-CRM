from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Factor
from .serializers import FactorSerializer


class FactorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Factor.objects.prefetch_related('items__product').all()
    serializer_class = FactorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class FactorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Factor.objects.prefetch_related('items__product').all()
    serializer_class = FactorSerializer
    permission_classes = [IsAuthenticated]
