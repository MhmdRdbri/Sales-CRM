from django.shortcuts import render
from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer
from rest_framework.permissions import *
from rest_framework.exceptions import PermissionDenied



class NoticeList(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]
    
    

    def get(self, request, *args, **kwargs):      
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission post any notice.")
        
        return self.create(request, *args, **kwargs)




class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        notice = self.get_object()
        send_datetime = datetime.combine(notice.send_date, notice.send_time)
        
        if now() > send_datetime:
            raise PermissionDenied("You cannot modify a notice that has already been sent.")
        
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission put change this notice.")
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user.profile.work_position != 'system_manager' and self.request.user.profile.work_position != 'admin':
            raise PermissionDenied("You do not have permission delete this  notice.")
        
        return self.destroy(request, *args, **kwargs)

