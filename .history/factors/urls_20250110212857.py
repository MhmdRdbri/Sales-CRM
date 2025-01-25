from django.urls import path
from .views import FactorListCreateView

app_name = 'factors'
urlpatterns = [
    path('factors/', FactorListCreateView.as_view(), name='factor-list-create'),
]
