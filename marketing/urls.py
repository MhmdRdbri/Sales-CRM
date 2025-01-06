from django.urls import path
from .views import *

app_name = 'marketing'


urlpatterns = [
    path('', MarketingList.as_view(), name='Marketing-list'),
    path('<int:pk>', MarketingDetail.as_view(), name='Marketing-detail'),
]