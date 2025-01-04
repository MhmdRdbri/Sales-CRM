from rest_framework import generics
from .models import CustomerProfile
from .serializers import *
from rest_framework.permissions import *

class CustomerProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

class CustomerProfileRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    
    def destroy(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.work_position == 'employee':
            raise PermissionDenied("Employees are not allowed to delete customer profiles.")
        
        return super().destroy(request, *args, **kwargs)