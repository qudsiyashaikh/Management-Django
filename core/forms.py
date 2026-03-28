from django import forms
from .models import CustomUser, Patient

# 1. Registration Form (Jo aapne manga)
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Create Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'contact', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

# 2. Patient Form (Iske bina aapka error nahi jayega)
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__' # Ya specific fields jo aapne model mein banaye hain