from django.contrib import admin
from .models import Doctor, Department, Patient, Medicine, Bill, Appointment # Saare models import karein

# In sab ko register karein
admin.site.register(Department) # <--- Yeh line zaroori hai
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Bill)
admin.site.register(Appointment)