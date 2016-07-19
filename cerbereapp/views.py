from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response
from .models import *
from .forms import *


## Index
## ##############################
def index(request):
    return render(request, "index.html")


## Account
## ##############################
@login_required
def account(request):
    employees_list = Employee.objects.all().count
    account_name = AccountType.objects.get(user_id = request.user.id)
    context = {
        'page_title': 'account',
        'employees_counter': employees_list,
        'username': request.user.username,
        'account_name' : AccountType.objects.get(user_id = request.user.id),
        'limit_employees': account_name.limit_employees,
    }
    return render(request, 'account.html', context)


## Dashboard
## ##############################
@login_required
def dashboard(request):
    employees_list = Employee.objects.all()
    context = {
        'page_title': 'Dashboard',
        'employees_list': employees_list,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)


## Document models
## ##############################
@login_required
def documentmodels_list(request):
    context = {
        'page_title': 'Document Models',
        'username': request.user.username,
        'documentmodels': DocumentModel.objects.all(),
        'form': DocumentModelForm(request.POST)
    }
    if request.method == "POST":
        form = DocumentModelForm(request.POST)
        if form.is_valid():
            new_documentmodel = DocumentModel.objects.create(
                user_id=request.user,
                name=form.cleaned_data.get('name'),
                warning_days=form.cleaned_data.get('warning_days'),
                critical_days=form.cleaned_data.get('critical_days')
            )
            new_documentmodel.save()
    return render(request, 'documentmodels_list.html', context)


@login_required
def documentmodel_details(request, documentmodel_id):
    context = {
        'page_title': 'Document model details',
        'documentmodel': DocumentModel.objects.get(pk=documentmodel_id),
    }
    return render(request, 'documentmodel_details.html', context)


@login_required
def documentmodel_new(request):
    form = DocumentModelForm()
    context = {
        'page_title': 'New document model',
        'form': DocumentModelForm(request.POST)
    }
    if request.method == "POST":
        if form.is_valid():
            new_documentmodel = DocumentModel.objects.create(
                user_id=request.user,
                name=form.cleaned_data.get('name'),
                warning_days=form.cleaned_data.get('warning_days'),
                critical_days=form.cleaned_data.get('critical_days')
            )
            new_documentmodel.save()
    return render(request, 'documentmodel_details.html', context)


## Employees
## ##############################
@login_required
def employees_list(request):
    context = {
        'page_title': 'Employees',
        'username': request.user.username,
        'employees': Employee.objects.all()
    }
    return render(request, 'employees_list.html', context)


@login_required
def employee_details(request, employee_id):
    context = {
        'page_title': 'Employee details',
        'employee': Employee.objects.get(pk=employee_id),
        'profiles': Profile.objects.all(),
    }
    return render(request, 'employee_details.html', {'form': MessageForm()})


@login_required
def employee_new(request):
    context = {
        'page_title': 'New Employee',
        'profiles': Profile.objects.all(),
    }
    return render(request, 'employee_new.html',  {'form': EmployeeForm()})


## Profiles
## ##############################
@login_required
def profiles_list(request):
    context = {
        'page_title': 'Profiles',
        'username': request.user.username,
        'profiles': Profile.objects.all(),
    }
    return render(request, 'profiles_list.html', context)


@login_required
def profile_details(request, profile_id):
    context = {
        'page_title': 'Profile details',
        'profile': Profile.objects.get(pk=profile_id),
    }
    return render(request, 'profile_details.html', context)
