from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response
from .models import *

def index(request):
    return render_to_response("index.html")

def dashboard(request):
    employees_list = Employee.objects.all()
    context = {
        'employees_list': employees_list,
    }
    return render_to_response("dashboard.html", context)
