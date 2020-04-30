from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def login_page(request):
    return render(request, "login.html")

def register_form(request):
    errors=User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, err in errors.items():
            messages.error(request, err)
        return redirect("/")

        
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    created_user=User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
    )
    #creates session keys and values
    request.session["user_id"]=created_user.id
    request.session["first_name"]=created_user.first_name # inserted

    return redirect("/success")

def home_page(request):
    if "user_id" not in request.session:
        messages.error(request, "Please login or register first.")
        return redirect("/")
    context={
        "user":User.objects.get(id=request.session["user_id"])
    }
    return render(request, "home-page.html", context)

def login_form(request):
    potential_users=User.objects.filter(email=request.POST['email'])
    
    if len(potential_users)==0:
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    user=potential_users[0]
    #checks password
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please check your email and password.")

        return redirect("/")
    #assigns session keys and values
    request.session["user_id"]=user.id
    request.session["first_name"]=user.first_name #inserted
    return redirect("/home")


def logout(request):
    request.session.pop("user_id")
    request.session.pop("first_name")

    return redirect("/")

def payment(request):
    potential_users=User.objects.filter(id=request.POST['user_id'])
    
    if len(potential_users)==0:
        messages.error(request, "Please check your email and password.")

        return redirect("/")

    user=potential_users[0]
    #checks password
    if not bcrypt.checkcard(request.POST['card'].encode(), user.card.encode()):
        messages.error(request, "Please enter a valid card for payment.")

        return redirect("/")
    #assigns session keys and values
    request.session["user_id"]=user.id
    request.session["first_name"]=user.first_name #inserted
    return redirect("/home")