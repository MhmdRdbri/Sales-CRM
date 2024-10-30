from django.urls import path
from .views import *

app_name = 'accountemployee'

urlpatterns = [
    path('employee-login/', CustomUserLoginAPIView.as_view(), name='employee-login'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/request-authenticated/', AuthenticatedPasswordResetRequestView.as_view(), name='password-reset-request-authenticated'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
]