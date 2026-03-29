from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Appointment, Bill, Medicine, Report
from .models import Appointment, Doctor
from django.utils import timezone
from .models import Appointment, Patient, Doctor
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Models import (Ek hi baar mein saare models)

from .models import (

    Doctor, Department, Appointment,

    Bill, Medicine, Patient, CustomUser

)



# Forms import

from .forms import PatientForm, RegistrationForm


def create_admin_silently(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "Admin@123")
        return HttpResponse("Admin Created! Username: admin, Pass: Admin@123")
    else:
        return HttpResponse("Admin already exists.")
# ---------------- USERS AUTH (Fixed) ----------------



# 1. Register View: Fixed to handle hashing & auto-login

def register_view(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            # Form validate hone ke baad, ise secure tarah se save karein

            user = form.save(commit=False)

            user.username = form.cleaned_data['email'] # Email ko hi username set kar rahe hain

            # Password hashing aur saving automaticaly form handling mein hota hai is_valid check ke baad jab user.save use karte hain:

            user.set_password(form.cleaned_data['password']) # Security hash set karein

            user.save()



            # Automatic Login: Register karte hi dashboard par bhej denge

            authenticate_user = authenticate(request, username=user.username, password=form.cleaned_data['password'])

            if authenticate_user is not None:

                login(request, authenticate_user) # Session start

                # Yahan Dashboard par redirect set hai:

                return redirect('dashboard')

            else:

                # Agar authenticate fail ho (highly unlikely but check handles duplicate issues), toh error

                return render(request, 'register.html', {'form': form, 'error': 'Auto-login failed after registration.'})



        # Agar form is_valid() fail ho jaye (e.g., passwords don't match)

        return render(request, 'register.html', {'form': form})



    else:

        # GET request ke liye khaali form

        form = RegistrationForm()

       

    return render(request, 'register.html', {'form': form})





# 2. Login View: Standard secure authenticate uses

def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email')

        password = request.POST.get('password')

       

        # Django built-in authenticate automatically looks for hashed passwords

        user = authenticate(request, username=email, password=password)

       

        if user is not None:

            login(request, user) # Start Session

            # Yahan bhi Dashboard par redirect set hai:

            return redirect('dashboard')

        else:

            return render(request, 'login.html', {'error': 'Invalid Email or Password'})

           

    return render(request, 'login.html')







def edit_user(request, id):

    user_obj = get_object_or_404(CustomUser, id=id)

   

    if request.method == "POST":

        user_obj.full_name = request.POST.get('full_name')

        user_obj.email = request.POST.get('email')

        user_obj.contact = request.POST.get('contact')

        user_obj.save()

        return redirect('all_users')

       

    return render(request, 'edit_user.html', {'user_to_edit': user_obj})



def delete_user(request, id):

    user_obj = get_object_or_404(CustomUser, id=id)

    user_obj.delete()

    return redirect('all_users')



# ---------------- Register ----------------



def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get('full_name')

        email = request.POST.get('email')

        password = request.POST.get('password')

        contact = request.POST.get('contact')



        # Yahan error "Email and Password are required" nahi aayega ab

        if not email or not password:

            return render(request, 'register.html', {'error': 'Email and Password are required!'})



        try:

            # Username=email dena zaroori hai

            user = CustomUser.objects.create_user(

                username=email,

                email=email,

                password=password,

                full_name=full_name,

                contact=contact

            )

            login(request, user)

            return redirect('dashboard')

        except Exception as e:

            return render(request, 'register.html', {'error': f'Registration failed: {e}'})



    return render(request, 'register.html')



# ---------------- DASHBOARD ----------------



def dashboard(request):
    # Counts
    doc_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    app_count = Appointment.objects.count()
    med_count = Medicine.objects.count()

    # Revenue Calculation
    revenue = Bill.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0

    # Recent Patients (Database se last 5 patients)
    recent_patients = Patient.objects.all().order_by('-id')[:5]

    # Dashboard ke liye appointments (Sahi variable name 'today_appointments' rakha hai)
    # Order by -id kiya hai taaki naya appointment sabse upar dikhe
    today_appointments = Appointment.objects.all().order_by('-id')[:5]

    context = {
        'doc_count': doc_count,
        'patient_count': patient_count,
        'app_count': app_count,
        'med_count': med_count,
        'revenue': revenue,
        'recent_patients': recent_patients,
        'today_appointments': today_appointments, # Variable ka naam HTML se match kar diya
    }
    return render(request, 'dashboard.html', context)


# ---------------- PATIENTS CRUD ----------------

# 1. Patients List

def patients_list(request):

    patients = Patient.objects.all().order_by('-id')

    # Agar aapki file 'patients.html' folder ke andar hai toh 'patients/patients.html' likhein

    # Agar direct templates mein hai toh 'patients.html' hi rehne dein

    return render(request, 'patients/patients.html', {'patients': patients})



# 2. Add Patient

def add_patient(request):

    if request.method == 'POST':

        form = PatientForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('patients')

    else:

        form = PatientForm()

   

    return render(request, 'patients/add_patient.html', {'form': form})



# 3. Edit Patient

def edit_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':

        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():

            form.save()

            return redirect('patients')

    else:

        form = PatientForm(instance=patient)

   

    return render(request, 'patients/add_patient.html', {'form': form})



# 4. Delete Patient

def delete_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    patient.delete()

    return redirect('patients')



# ---------------- DOCTORS CRUD ----------------



# 1. Doctors List View

def all_doctors(request):

    doctors_list = Doctor.objects.all().order_by('-id')

    print(f"DEBUG: Total Doctors in DB: {doctors_list.count()}")

    return render(request, 'doctor.html', {'doctors': doctors_list})



# 2. Add Doctor View

def add_doctor(request):

    departments = Department.objects.all()

    if request.method == "POST":

        name = request.POST.get('name')

        spec = request.POST.get('specialization')

        mob = request.POST.get('mobile')

        email = request.POST.get('email')

        dept_id = request.POST.get('department')



        if name and dept_id:

            dept_obj = Department.objects.get(id=dept_id)

            Doctor.objects.create(

                name=name, specialization=spec,

                mobile=mob, email=email, department=dept_obj

            )

            return redirect('all_doctors')

    return render(request, 'add_doctor.html', {'departments': departments})



# 3. Edit Doctor View

def edit_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    departments = Department.objects.all()

   

    if request.method == "POST":

        doctor.name = request.POST.get('name')

        doctor.specialization = request.POST.get('specialization')

        doctor.mobile = request.POST.get('mobile')

        doctor.email = request.POST.get('email')

       

        dept_id = request.POST.get('department')

        if dept_id:

            doctor.department = Department.objects.get(id=dept_id)

           

        doctor.save()

        return redirect('all_doctors')

       

    # Yahan 'doctor' object pass kar rahe hain taaki form mein purana data dikhe

    return render(request, 'add_doctor.html', {'doctor': doctor, 'departments': departments})



# 4. Delete Doctor View

def delete_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    doctor.delete()

    return redirect('all_doctors')



# ---------------- DEPARTMENTS ----------------

def departments_list(request):

    depts = Department.objects.all()

    return render(request, 'departments.html', {'departments': depts})



def add_department(request):

    if request.method == "POST":

        dept_name = request.POST.get('dept_name')

        dept_desc = request.POST.get('dept_desc')

        Department.objects.create(name=dept_name, description=dept_desc)

        return redirect('departments_list')

    return render(request, 'add_department.html')



# ---------------- APPOINTMENTS ----------------

def all_appointments(request):

    # 'date' aur 'time' ke hisab se sort kiya hai taaki upar naye appointments dikhein

    appointments = Appointment.objects.all().order_by('date', 'time')

    return render(request, 'appointments.html', {'appointments': appointments})



# Add Appointment View

def add_appointment(request):

    if request.method == "POST":

        p_name = request.POST.get('patient_name')

        d_id = request.POST.get('doctor')

        a_date = request.POST.get('date')

        a_time = request.POST.get('time')

        a_reason = request.POST.get('reason')

       

        # get_object_or_404 use kiya hai taaki agar doctor na mile toh error na aaye

        doc = get_object_or_404(Doctor, id=d_id)

       

        Appointment.objects.create(

            patient_name=p_name,

            doctor=doc,

            date=a_date,

            time=a_time,

            reason=a_reason,

            status='Pending' # Default status set kar diya

        )

        # Ensure karein ki urls.py mein name='all_appointments' hi ho

        return redirect('all_appointments')



    all_docs = Doctor.objects.all()

    return render(request, 'add_appointment.html', {'doctors': all_docs})



# ---------------- USERS (Fixed missing function) ----------------

def all_users(request):

    users_list = CustomUser.objects.all()

    return render(request, 'users.html', {'users': users_list})



# ---------------- BILLING & MEDICINES ----------------

def all_bills(request):

    bills = Bill.objects.all().order_by('-date')

    total_revenue = Bill.objects.filter(status='Paid').aggregate(Sum('total'))['total__sum'] or 0

    pending_count = Bill.objects.filter(status='Unpaid').count()

    return render(request, 'billing.html', {

        'bills': bills,

        'total_revenue': total_revenue,

        'pending_count': pending_count

    })



def all_medicines(request):

    medicines = Medicine.objects.all().order_by('name')

    return render(request, 'medicines.html', {'medicines': medicines})



# ---------------- REPORTS & PROFILE ----------------

def hospital_report(request):

    # Sabhi data uthayein

    doctors = Doctor.objects.all()

    patients = Patient.objects.all()

    appointments = Appointment.objects.all()

   

    # ERROR FIX: Yahan 'total' ki jagah 'amount' likha hai

    total_revenue = Bill.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0

   

    context = {

        'doctors': doctors,

        'patients': patients,

        'appointments': appointments,

        'total_revenue': total_revenue,

    }

    return render(request, 'reports.html', context)



#@login_required

def user_profile(request):

    return render(request, 'profile.html', {'user': request.user})



def user_logout(request):

    logout(request)

    return redirect('login')



def appointments_view(request):

    data = Appointment.objects.all().order_by('-date')

    return render(request, 'core/appointments.html', {'appointments': data})



def billing_view(request):

    bills = Bill.objects.all().order_by('-date')

    return render(request, 'core/billing.html', {'bills': bills})



def medicines_view(request):

    meds = Medicine.objects.all()

    return render(request, 'core/medicines.html', {'medicines': meds})



def reports_view(request):

    reps = Report.objects.all()

    return render(request, 'core/reports.html', {'reports': reps})





def all_bills(request):

    bills = Bill.objects.all().order_by('-date') # Date ke hisab se sort karein

    return render(request, 'billing.html', {'bills': bills})
