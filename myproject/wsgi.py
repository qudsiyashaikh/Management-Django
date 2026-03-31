"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()

# --- YAHAN SE COPY KARO ---
try:
    from core.models import Department
    # Ye departments khud ban jayenge
    depts = ['Cardiology', 'Neurology', 'Orthopedics', 'General Medicine']
    for dept_name in depts:
        Department.objects.get_or_create(name=dept_name)
    print("Departments added successfully!")
except Exception as e:
    print(f"Error adding departments: {e}")