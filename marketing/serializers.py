from rest_framework import serializers 
from .models import *

class MarketingSerializer(serializers.ModelSerializer):
    
    class Meta:
        mdoel = Marketing
        fields = ["id","campaign_name","start_date","end_date","message","target_audiences"]