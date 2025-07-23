from django.urls import path
from .views import LoginView, LogutView, Registerview

urlpatterns = [
    path("register", Registerview.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogutView.as_view(), name="logout"),
]
