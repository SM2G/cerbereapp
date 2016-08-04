from django.http import HttpResponse, request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from .models import *
from .forms import *


## Index
## #############################################################################
def index(request):
    return render(request, "index.html")


## Account
## #############################################################################
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
## #############################################################################
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
## #############################################################################
#@login_required
#def documentmodels_list(request, template_name='documentmodels_list.html'):
#    logged_user=str(request.user.id)
#    documentmodels = DocumentModel.objects.all().filter(user_id=request.user)
#    ctx = {}
#    ctx['documentmodels'] = documentmodels
#    return render(request, template_name, ctx)

@login_required
def documentmodels_list(request, template_name='documentmodels_list.html'):
    logged_user=str(request.user.id)
    documentmodels = DocumentModel.objects.all().filter(user_id=request.user)
    for documentmodel in documentmodels:
        print(documentmodel)
        print(documentmodel.profile_set.all())
    ctx = {}
    ctx['documentmodels'] = documentmodels
    return render(request, template_name, ctx)


@login_required
def documentmodel_create(request, template_name='documentmodel_create.html'):
    logged_user=str(request.user.id)
    form = DocumentModelForm(request.POST or None)
    if form.is_valid():
        form.instance.user_id = request.user
        form.save()
        return redirect('documentmodels_list')
    ctx = {}
    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def documentmodel_update(request, documentmodel_id, template_name='documentmodel_update.html'):
    documentmodel = get_object_or_404(DocumentModel, pk=documentmodel_id)
    form = DocumentModelForm(request.POST or None, instance=documentmodel)
    if form.is_valid():
        form.save()
        return redirect('documentmodels_list')
    ctx = {}
    ctx["form"] = form
    ctx["documentmodel"] = documentmodel
    return render(request, template_name, ctx)


@login_required
def documentmodel_delete(request, documentmodel_id):
    logged_user=str(request.user.id)
    trash = DocumentModel.objects.get(pk=documentmodel_id)
    trash.delete()
    ctx = {
        #'page_title': 'Document Models',
        'documentmodels': DocumentModel.objects.all().filter(user_id=request.user),
        'form': DocumentModelForm(request.POST)
    }
    return render(request, 'documentmodels_list.html', ctx)


## Profiles
## #############################################################################
@login_required
def profiles_list(request, template_name='profiles_list.html'):
    logged_user=str(request.user.id)
    profiles = Profile.objects.all().filter(user_id=request.user)
    ctx = {}
    ctx['profiles'] = profiles
    return render(request, template_name, ctx)


@login_required
def profile_create(request, template_name='profile_create.html'):
    logged_user=int(request.user.id)
    print('======= logged_user: ', logged_user)
    form = ProfileForm(request.POST or None, logged_user=logged_user)
    if form.is_valid():
        form.instance.user_id = request.user
        form.save()
        return redirect('profiles_list')
    ctx = {}
    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def profile_update(request, pk, template_name='profile_update.html'):
    logged_user=str(request.user.id)
    profile = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(request.POST or None, logged_user=logged_user, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('profiles_list')
    return render(request, template_name, {'form':form})


@login_required
def profile_delete(request, profile_id):
    logged_user=str(request.user.id)
    trash = Profile.objects.get(pk=profile_id)
    trash.delete()
    ctx = {
        'logged_user': logged_user,
        'username': request.user.username,
        'profiles': Profile.objects.all().filter(user_id=request.user),
        'form': ProfileForm(request.POST, logged_user=logged_user, instance=trash)
    }
    return render(request, 'profiles_list.html', ctx)


## Employees
## #############################################################################
@login_required
def employees_list(request, template_name='employees_list.html'):
    logged_user = str(request.user.id)
    employees = Employee.objects.all().filter(user_id=request.user).order_by("is_active")
    ctx = {}
    ctx['employees'] = employees
    return render(request, template_name, ctx)


@login_required
def employee_create(request, template_name='employee_create.html'):
    logged_user=str(request.user.id)
    form = EmployeeForm(request.POST or None, logged_user=logged_user)
    if form.is_valid():
        form.instance.user_id = request.user
        print('======= Using profile', form.instance.profile_id.id)
        form.save()
        employee_id = form.instance
        print('======= Creating agent', form.data)
        for documentmodel in form.instance.profile_id.documentmodels_list.all():
             print('======= creating actual document', documentmodel,'...')
             new_document = ActualDocument(employee = employee_id, documentmodel = documentmodel)
             new_document.save()
        return redirect('employees_list')
    ctx = {}
    ctx["form"] = form
    return render(request, template_name, ctx)


@login_required
def employee_update(request, employee_id, template_name='employee_update.html'):
    logged_user = str(request.user.id)
    employee = get_object_or_404(Employee, pk = employee_id)
    form = EmployeeForm(request.POST or None, logged_user = logged_user, instance = employee)
    print('======= Employee id', employee.id)
    actualdocument_list = ActualDocument.objects.all().filter(employee_id = employee.id)
    #print('======= actualdocument_list', actualdocument_list)

    actualdocuments = {}
    for actualdocument in actualdocument_list:
        #k = actualdocument.documentmodel.name
        k = get_object_or_404(ActualDocument, pk = actualdocument.id)
        #print('======= actualdocument.id', actualdocument.id)
        #v = get_object_or_404(ActualDocument, pk = actualdocument.id)
        actualdocuments[k] = ActualDocumentForm(request.POST or None, logged_user = logged_user, instance = k)

    if form.is_valid():
        print('======= CHECKING FORM:',form)
        form.save()
        return redirect('employees_list')

    endsave = len(actualdocuments.keys())

    for k, v in actualdocuments.items():
        print('======= CHECKING V:',v)
        if v.is_valid():
            print('======= SAVING FORM!!!')
            v.save()
            #print('======= Remains to save ',endsave,'...')
            endsave -= 1
        if endsave == 0:
            return redirect('employees_list')

    ctx = {}
    ctx["form"] = form
    ctx["actualdocuments"] = actualdocuments
    print('======= DICT ', actualdocuments)
    return render(request, template_name, ctx)


@login_required
def employee_delete(request, employee_id):
    logged_user=str(request.user.id)
    trash = Employee.objects.get(pk=employee_id)
    trash.delete()
    ctx = {
        'logged_user': logged_user,
        'username': request.user.username,
        'employees': Employee.objects.all().filter(user_id=request.user),
    }
    return render(request, 'employees_list.html', ctx)
