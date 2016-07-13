from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response
from .models import *


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    employees_list = Employee.objects.all()
    context = {
        'employees_list': employees_list,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)


@login_required
def documentmodel(request):
    context = {
        'username': request.user.username,
        'user_id': request.user.id
    }
    return render(request, 'documentmodel.html', context)
