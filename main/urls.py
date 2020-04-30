from django.urls import path
from . import views

urlpatterns=[
    path("", views.login_page),
    path("home", views.home_page),
    path("register", views.register_form),
    path("login", views.login_form),
    path("logout", views.logout),
    path("payment", views.payment),

]