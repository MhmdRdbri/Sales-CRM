from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOpportunityViewSet

app_name = 'salesopportunities'

router = DefaultRouter()
router.register(r'sales-opportunities', SalesOpportunityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]