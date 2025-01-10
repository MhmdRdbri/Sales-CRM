from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Factors
from .serializers import FactorSerializer
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied



v




class FactorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Factors.objects.all()
    serializer_class = FactorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'accountant' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission get this factor.")
        
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'accountant' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission put change this factor.")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'accountant' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission delete this factor.")
        
        return self.destroy(request, *args, **kwargs)

