from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accountemployee.urls', namespace='account')),
]
