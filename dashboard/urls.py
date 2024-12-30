from django.urls import path
from .views import *

app_name = 'dashboard'


urlpatterns = [
    path('', DashboardDetail.as_view(), name='Marketing-list'),

]