from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.views import View
from .models import User
from django.contrib.auth import login, logout, authenticate


class Registerview(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "auth/register.html", {"form": form})
    
    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("products-list")
        return render(request, "auth/register.html", {"form": form})
    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data.get("email_or_phone")
            password = form.cleaned_data.get("password")
            user = authenticate(request=request, email=email_or_phone, password=password)
            if user is None:
                user = User.objects.filter(phone_number=email_or_phone).first()
                if user and user.check_password(password):
                    login(request, user)
                else:
                    print("user not found")
            else:
                login(request, user)
        return redirect("products-list")

class LogutView(View):
    def get(self, request):
        logout(request=request)
        return redirect("products-list")


