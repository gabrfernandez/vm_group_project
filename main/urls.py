from django.urls import path
from . import views

urlpatterns=[
    path("", views.login_page),
    path("home", views.home_page),
]