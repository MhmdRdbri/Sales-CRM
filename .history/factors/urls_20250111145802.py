from django.urls import path
from .views import *
from django.urls import path
from .views import FactorListCreateAPIView, FactorRetrieveAPIView

app_name = 'factors'

urlpatterns = [
    path('factors/', FactorListCreateAPIView.as_view(), name='factor-list-create'),
    path('factors/<int:pk>/', FactorRetrieveAPIView.as_view(), name='factor-retrieve'),
]
