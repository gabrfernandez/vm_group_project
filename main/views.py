from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def login_page(request):
    return render(request, "login.html")

def home_page(request):
    return render(request, "home-page.html")