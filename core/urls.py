from django.urls import path
from . import views

urlpatterns = [
    # --- Authentication ---
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'), 
    path('user/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('user/delete/<int:id>/', views.delete_user, name='delete_user'),
   
   
    # --- Dashboard ---
    path('dashboard/', views.dashboard, name='dashboard'),

    # --- Patients ---
    path('patients/', views.patients_list, name='patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),

    # --- Doctors ---
    # Sidebar mein 'all_doctors' hai, isliye name='all_doctors' rakha hai
    path('doctor/', views.all_doctors, name='all_doctors'), 
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctor/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('doctor/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
   
    # --- Departments ---
    path('departments/', views.departments_list, name='departments'), 
    path('add-department/', views.add_department, name='add_department'),
    # --- Appointments ---
    # core/urls.py
    path('appointments/', views.all_appointments, name='all_appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    # --- Billing ---
    path('billing/', views.all_bills, name='billing'),

    # --- Other Modules ---
    # Sidebar mein 'all_users' hai, isliye name='all_users' rakha hai
    path('users/', views.all_users, name='all_users'),
    path('medicines/', views.all_medicines, name='medicines'),
    path('reports/', views.hospital_report, name='reports'),
    path('profile/', views.user_profile, name='profile'),
]