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
        # Debugging print to check user's work_position
        print(f"User's work_position: {getattr(request.user.profile, 'work_position', 'No Profile')}")

        # Check if the user's profile work_position is 'employee'
        if hasattr(request.user, 'profile') and request.user.profile.work_position == 'regular':
            raise PermissionDenied("Employees are not allowed to delete customer profiles.")
        
        # Proceed with deletion if user is allowed
        return super().destroy(request, *args, **kwargs)