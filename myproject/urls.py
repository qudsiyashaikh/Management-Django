from django.contrib import admin
from django.urls import path, include
from core.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Core app URLs
    path('', include('core.urls')),
]