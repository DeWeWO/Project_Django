import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage, Category
from .forms import ProductForm
from django.db.models import Avg, Max, Min, Sum, F, ExpressionWrapper, DecimalField, Value, Case, When, Q
from django.db.models.functions import Round
from django.core.paginator import Paginator



def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save()
            images = form.cleaned_data.get("images")
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect("products-list")
    return render(request, "shop/add_product.html", {"form": form})
    

def product_list(request, category_slug = None):
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    search = request.GET.get("search")
    if search:
        products = products.filter(Q(title__icontains=search) | Q(description__icontains=search))
    products.annotate(
        sum_discount=Sum("discount__percent"),
        new_price = ExpressionWrapper(
            Round((100 - F("sum_discount")) * F("price") / 100, 2),
        output_field=DecimalField(decimal_places=2, max_digits=12))).order_by("-id")
    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    return render(request, "shop/products.html", {"products": products})

def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, "shop/product_detail.html", {"product": product})

def product_update(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    form = ProductForm(instance=product)
    product_images = ProductImage.objects.filter(product=product)
    if request.method == "POST":
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save()
            images = form.cleaned_data.get("images")
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect("products-list")
    return render(request, "shop/update_product.html", {"form": form, "product_images": product_images})

def product_delete(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    product.delete()
    return redirect("products-list")



def index(request):
    return render(request, "furni/index.html")

def about(request):
    return render(request, "furni/about.html")

def contact(request):
    BOT_TOKEN = "8137226513:AAELQDpI4TXlLDbFsDLpcZ6ZYjvP1UIvaDk"
    GROUP_CHAT_ID = -4890613070
    URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        message = request.POST.get("message")
        text = f"<b>First Name: {fname}\nLast Name: {lname}\nEmail: {email}\nMessage:</b> <i>{message}</i>"
        response = requests.post(url=URL, data={
            "chat_id": GROUP_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        })
        print(response)
    return render(request, "furni/contact.html")
