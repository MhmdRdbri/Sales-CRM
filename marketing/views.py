from django.shortcuts import render
from rest_framework import generics
from .models import Marketing
from .serializers import MarketingSerializer
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied



class MarketingList(generics.ListCreateAPIView):
    queryset = Marketing.objects.all()
    serializer_class = MarketingSerializer
    permission_classes = [IsAuthenticated]
    
    

    def get(self, request, *args, **kwargs):      
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission post any marketing campaign.")
        
        return self.create(request, *args, **kwargs)




class MarketingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marketing.objects.all()
    serializer_class = MarketingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission put change this Marketing campaign.")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission delete this  Marketing campaign.")
        
        return self.destroy(request, *args, **kwargs)

