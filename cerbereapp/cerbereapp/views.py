from django.http import HttpResponse
from django.contrib.auth import logout
from .models import Employee

from django.shortcuts import render, render_to_response

def dashboard(request):
    return render_to_response("dashboard.html",{'all_employees': Employee.objects.all()})

def index(request):
    return render_to_response("index.html")

def login(request):
    return render_to_response("login.html")

def logout(request):
    logout(request)
    # Redirect to a success page.

def signup(request):
    return render_to_response("signup.html")
