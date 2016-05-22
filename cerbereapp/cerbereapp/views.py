from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import Employee

from django.shortcuts import render, render_to_response

def dashboard(request):
    return render_to_response("dashboard.html",{'all_employees': Employee.objects.all()})

def index(request):
    return render_to_response("index.html")

def login(request):
    return render_to_response("login.html")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return render_to_response("dashboard.html")
        else:
            # Return a 'disabled account' error message
            return render_to_response("login.html")
    else:
        # Return an 'invalid login' error message.
        return render_to_response("login.html")


def logout(request):
    logout(request)
    # Redirect to a success page.

def signup(request):
    return render_to_response("signup.html")
