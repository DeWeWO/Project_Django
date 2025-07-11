from django.urls import path
from .views import index, about, contact, product_list, product_detail, add_product, product_delete, product_update

urlpatterns = [
    path('', index, name="index"),
    path("add/product/", add_product, name="add_product"),
    path("update/product/<slug:product_slug>/", product_update, name="product_update"),
    path("delete/product/<slug:product_slug>/", product_delete, name="product_delete"),
    path("products/", product_list, name="products-list"),
    path("products/<slug:category_slug>/", product_list, name="products-list-by-cat"),
    path("product/<slug:product_slug>/", product_detail, name="product_detail"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
]