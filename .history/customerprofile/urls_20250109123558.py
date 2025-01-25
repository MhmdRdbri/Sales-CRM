from django.urls import path
from .views import *

app_name = 'customerprofile'

urlpatterns = [
    path('customers/', CustomerProfileListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerProfileRetrieveUpdateDeleteView.as_view(), name='customer-detail'),
    path('upload-customers/', UploadCustomerProfilesView.as_view(), name='upload-customers'),
]
]