from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
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
    account_name = AccountType.objects.get(user_id = request.user.id)
    context = {
        'page_title': 'account',
        'employee_counter': Employee.objects.all().filter(user_id=request.user).count,
        'username': request.user.username,
        'account_name' : AccountType.objects.get(user_id = request.user.id),
        'limit_employees': account_name.limit_employees,
    }
    return render(request, 'account.html', context)


## Dashboard
## ##############################
@login_required
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'employee_counter': Employee.objects.all().filter(user_id=request.user).count,
        'profile_counter': Profile.objects.all().filter(user_id=request.user).count,
        'documentmodel_counter': DocumentModel.objects.all().filter(user_id=request.user).count,
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
        'documentmodels': DocumentModel.objects.all().filter(user_id=request.user),
        'form': ProfileFormCreate(request.POST or None)
    }
    if request.method == "POST":
        form = DocumentModelFormCreate(request.POST)
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
def documentmodel_create(request, template_name='documentmodel_create.html'):
    print('====== Entering')
    form = DocumentModelFormCreate(request.POST or None)
    if form.is_valid():
        print('====== Going to save')
        form.save()
        return redirect('documentmodels_list')
    print('====== Render')
    return render(request, template_name, {'form':form})



@login_required
def documentmodel_trash(request, documentmodel_id):
    trash = DocumentModel.objects.get(pk=documentmodel_id)
    trash.delete()
    context = {
        'page_title': 'Document Models',
        'username': request.user.username,
        'documentmodels': DocumentModel.objects.all().filter(user_id=request.user),
        'form': DocumentModelFormCreate(request.POST)
    }
    return render(request, 'documentmodels_list.html', context)


@login_required
def documentmodel_update(request, pk, template_name='documentmodel_update.html'):
    documentmodel = get_object_or_404(DocumentModel, pk=pk)
    form = DocumentModelFormCreate(request.POST or None, instance=documentmodel)
    if form.is_valid():
        form.save()
        return redirect('documentmodels_list')
    return render(request, template_name, {'form':form})


## Profiles
## ##############################
@login_required
def profiles_list(request):
    context = {
        'page_title': 'Profiles',
        'username': request.user.username,
        'profiles': Profile.objects.all().filter(user_id=request.user),
        'form': ProfileFormCreate(request.POST or None)
    }
    if request.method == "POST":
        form = ProfileFormCreate(request.POST)
        if form.is_valid():
            new_profile = Profile.objects.create(
                user_id=request.user,
                name=form.cleaned_data.get('name')
            )
            new_profile.save()
    return render(request, 'profiles_list.html', context)


@login_required
def profile_create(request, template_name='profile_create.html'):
    form = ProfileFormCreate(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('profiles_list')
    return render(request, template_name, {'form':form})


@login_required
def profile_create(request):
    context = {
        'page_title': 'Profiles',
        'username': request.user.username,
        'form': ProfileFormCreate(request.POST or None)
    }
    if request.method == "POST":
        form = ProfileFormCreate(request.POST)
        if form.is_valid():
            new_profile = Profile.objects.create(
                user_id=request.user,
                name=form.cleaned_data.get('name')
            )
            new_profile.save()
    return render(request, 'profile_create.html', context)


def profile_trash(request, profile_id):
    trash = Profile.objects.get(pk=profile_id)
    trash.delete()
    context = {
        'page_title': 'Profile',
        'username': request.user.username,
        'profiles': Profile.objects.all().filter(user_id=request.user),
        'form': ProfileFormCreate(request.POST)
    }
    return render(request, 'profiles_list.html', context)


@login_required
def profile_update(request, profile_id):
    context = {
        'page_title': 'Profile update',
        'profile': Profile.objects.get(pk=profile_id),
    }
    return render(request, 'profile_update.html', context)

## Employees
## ##############################
@login_required
def employees_list(request):
    context = {
        'page_title': 'Employees',
        'username': request.user.username,
        'employees': Employee.objects.all().filter(user_id=request.user),
    }
    return render(request, 'employees_list.html', context)


@login_required
def employee_create(request, template_name='employee_create.html'):
    form = EmployeeFormCreate(request.POST or None)
    context = {
        'page_title': 'Employees',
        'username': request.user.username,
        'form': EmployeeFormCreate(request.POST or None)
    }
    if form.is_valid():
        form.save()
        return redirect('employees_list')
    return render(request, template_name, {'form':form})


@login_required
def employee_trash(request, employee_id):
    trash = Employee.objects.get(pk=employee_id)
    trash.delete()
    context = {
        'page_title': 'Employees',
        'username': request.user.username,
        'employees': Employee.objects.all().filter(user_id=request.user),
        'form': EmployeeFormCreate(request.POST)
    }
    return render(request, 'employees_list.html', context)


@login_required
def employee_update(request, employee_id):
    context = {
        'page_title': 'Employee update',
        'employee': Employee.objects.get(pk=employee_id),
        'profiles': Profile.objects.all(),
    }
    return render(request, 'employee_update.html')
