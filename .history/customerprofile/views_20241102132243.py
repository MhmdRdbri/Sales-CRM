from rest_framework import generics
from .models import CustomerProfile
from .serializers import *
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied

class CustomerProfileListCreateView(generics.ListCreateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

class CustomerProfileRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    
    def destroy(self, request, *args, **kwargs):
        print(f"User's work_position: {getattr(request.user.profile, 'work_position', 'No Profile')}")

        if hasattr(request.user, 'profile') and request.user.profile.work_position == 'regular':
            raise PermissionDenied("Employees are not allowed to delete customer profiles.")
        
        return super().destroy(request, *args, **kwargs)