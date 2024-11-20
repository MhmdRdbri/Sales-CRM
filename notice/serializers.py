from rest_framework import serializers 
from .models import *

class NoticeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notice
        fields = ["id","title","send_time","send_date","text","audiences"]