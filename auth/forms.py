from django.contrib.auth.forms import UserCreationForm as BaseCreationForm, UserChangeForm as BaseChangeForm
from .models import User
from django import forms
from phonenumber_field.formfields import PhoneNumberField


class UserCreationForm(BaseCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone_number")


class UserChangeForm(BaseChangeForm):
    class Meta:
        model = User
        fields = ("email", "phone_number")



class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label="Email / Phone number", max_length=255, required=True)
    password = forms.CharField(strip=False, required=True, widget=forms.TextInput(attrs={"class": "form-control", "type": "password"}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = PhoneNumberField(required=True)
    
    class Meta:
        model = User
        fields = ("email", "phone_number", "password1", "password2")
    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user
