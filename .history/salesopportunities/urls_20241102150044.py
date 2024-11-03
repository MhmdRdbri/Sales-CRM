from django.urls import path
from .views import *

app_name = 'salesopportunities'
router = DefaultRouter()
router.register(r'sales-opportunities', SalesOpportunityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]