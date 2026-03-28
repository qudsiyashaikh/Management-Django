from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings

# SIRF EK BAAR CustomUser define karein
class CustomUser(AbstractUser):
    # Email ko unique rakhna zaroori hai agar aap email se login chahte hain
    email = models.EmailField(unique=True) 
    
    full_name = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Yeh manager password hashing aur create_user() ke liye compulsory hai
    objects = UserManager() 

    def __str__(self):
        # Pehle email dikhaye, agar na ho toh username
        return self.email if self.email else self.username
# --- Baki Models ---

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    disease = models.CharField(max_length=200)
    admission_date = models.DateField()

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default="General")
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(default="Regular Checkup")
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ])

class Bill(models.Model):
    invoice_no = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')

    def __str__(self):
        return f"{self.invoice_no} - {self.patient_name}"

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    expiry_date = models.DateField()
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    



  # 1. Medicines Model
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __clstr__(self):
        return self.name

# 2. Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient_name = models.CharField(max_length=200)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

# 3. Billing Model
class Bill(models.Model):
    patient_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])

# 4. Reports Model
class Report(models.Model):
    patient_name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=100) # e.g., Blood Test, X-Ray
    file = models.FileField(upload_to='reports/')
    date = models.DateField(auto_now_add=True)  