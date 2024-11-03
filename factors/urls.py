from django.urls import path
from .views import *

app_name = 'factors'


urlpatterns = [
    path('', FactorList.as_view(), name='factor-list'),
    path('<int:pk>', FactorDetail.as_view(), name='factor-detail'),
]