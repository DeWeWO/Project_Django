from django.urls import path  
from .views import main_view, about_view, contact_view, products, users, login

urlpatterns = [
    path("", main_view, name="main"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
    path("products/", products, name="product"),
    path("products/<int:product_id>/", products, name="products"),
    path('users/', users, name='user'),
    path("users/<int:id>/<str:name>/", users, name="users"),
    path("login/", login, name='login')
]