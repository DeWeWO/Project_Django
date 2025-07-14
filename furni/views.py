import requests
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage, Category, Comment
from .forms import ProductForm, ProductUpdateForm
from django.db.models import Avg, Max, Min, Sum, F, ExpressionWrapper, DecimalField, Q
from django.db.models.functions import Round, Coalesce
from django.core.paginator import Paginator
from environs import Env
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


env = Env()
env.read_env()


@login_required(login_url="/auth/login/")
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            images = form.cleaned_data.get("images")
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            return redirect("products-list")
    return render(request, "shop/add_product.html", {"form": form})
    

def product_list(request, category_slug=None):
    products = Product.objects.select_related("category").all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    search = request.GET.get("search")
    if search:
        products = products.filter(Q(title__icontains=search) | Q(description__icontains=search))
    products = products.annotate(
        sum_discount=Coalesce(Sum("discount__percent"), 0),
        new_price=ExpressionWrapper(
            Round((100 - Coalesce(Sum("discount__percent"), 0)) * F("price") / 100, 2),
            output_field=DecimalField(decimal_places=2, max_digits=12)
        )
    ).order_by("-id")
    paginator = Paginator(products, 3)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)
    return render(request, "shop/products.html", {"products": products})


def product_detail(request, product_slug):
    product = Product.objects.filter(slug=product_slug).select_related("author").prefetch_related("images").first()
    if request.method == "POST":
        Comment.objects.create(author=request.user, product=product, message=request.POST["comment"])
    comments = Comment.objects.filter(product=product)
    return render(request, "shop/product_detail.html", {"product": product, "comments": comments})


@login_required(login_url="/auth/login/")
def product_update(request, product_slug):
    product = Product.objects.filter(slug=product_slug).select_related("author").first()
    if product.author == request.user:
        form = ProductUpdateForm(instance=product)
        product_images = ProductImage.objects.filter(product=product)
        if request.method == "POST":
            form = ProductUpdateForm(instance=product, data=request.POST, files=request.FILES)
            if form.is_valid():
                product = form.save()
                images = form.cleaned_data.get("images")
                for image in images:
                    ProductImage.objects.create(product=product, image=image)
                reverse_url = reverse("product_detail", args=(product.slug, ))
                return redirect(reverse_url)
        return render(request, "shop/update_product.html", {"form": form, "product_images": product_images})
    else:
        return HttpResponseForbidden("Siz bu mahsulotni tahrirlay olmaysiz!!")

@login_required(login_url="/auth/login/")
def product_delete(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    if product.author == request.user:
        product.delete()
        return redirect("products-list")
    else:
        return HttpResponseForbidden("Siz bu mahsulotni o'chira olmaysiz!!")



def index(request):
    return render(request, "furni/index.html")

def about(request):
    return render(request, "furni/about.html")

def contact(request):
    BOT_TOKEN = env.str("BOT_TOKEN")
    GROUP_CHAT_ID = env.str(GROUP_CHAT_ID)
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
