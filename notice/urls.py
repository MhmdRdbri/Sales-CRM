from django.urls import path
from .views import *

app_name = 'notice'


urlpatterns = [
    path('', NoticeList.as_view(), name='Marketing-list'),
    path('<int:pk>', NoticeDetail.as_view(), name='Marketing-detail'),
]