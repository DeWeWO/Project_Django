from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader


data = [
    {
        "name": "iPhone 17 Pro Max",
        "price": 1300,
        "quantity": 5
    },
    {
        "name": "iPhone 16 Pro Max",
        "price": 1200,
        "quantity": 4
    },
    {
        "name": "iPhone 15 Pro Max",
        "price": 1100,
        "quantity": 4.7
    },
    {
        "name": "iPhone 14 Pro Max",
        "price": 1000,
        "quantity": 4.5
    }
]

def main_view(request: HttpRequest):
    return render(request, 'core/index.html', context={"time": timezone.now(), "data": data})

def about_view(request: HttpRequest):
    return HttpResponse("<h1>About Page</h1><a href='/'>Main</a> <a href='/contact/'>Contact</a>")

def contact_view(request: HttpRequest):
    return render(request, 'core/contact.html')

def products(request, product_id=1):
    return HttpResponse(f"<h1>Mahsulot ID: {product_id}</h1>")

def users(request, id=1, name='DeWeW'):
    return HttpResponse(f"<h1>USER ID: {id}<br>USER NAME: {name}</h1>")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
    return render(request, "core/login.html")