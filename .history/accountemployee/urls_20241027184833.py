from django.urls import path
from .views import *

app_name = 'accountemployee'

urlpatterns = [
    path('employee-login/', CustomUserLoginAPIView.as_view(), name='user-login'),
    # path('reset-password/', PasswordResetInitiateAPIView.as_view(), name='initiate-reset-password'),
    # path('reset-password/verify/<str:token>/', PasswordResetVerifyAPIView.as_view(), name='verify-reset-password'),
    # path('register/', UserRegistrationView.as_view(), name='user-register'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    ]