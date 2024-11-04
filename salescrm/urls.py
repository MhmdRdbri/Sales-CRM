from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('accountemployee/', include('accountemployee.urls', namespace='accountemployee')),
    path('products/', include('products.urls', namespace='products')),
    path('customerprofile/', include('customerprofile.urls', namespace='customerprofile')),
    path('salesopportunities/', include('salesopportunities.urls', namespace='salesopportunities')),
    path('customerprofile/', include('customerprofile.urls', namespace='customerprofile')),  
    path('factors/', include('factors.urls', namespace='factors')),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
